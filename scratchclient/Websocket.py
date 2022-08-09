"""
Implements the WebSocket protocol
https://datatracker.ietf.org/doc/html/rfc6455

scratchclient used to use https://pypi.org/project/websocket-client/ but this was abandoned for three reasons:
- websocket-client has a naming problem that makes it difficult to build scratchclient from source in some environments
- It doesn't support asyncio, which is something I wanted; I found https://pypi.org/project/websockets/ but using both seemed like overkill
- The WebSocket protocol is pretty simple, so it seemed pointless to introduce a dependency for it

This does not implement the full protocol but it is enough for the purposes of this library. Some features (namely fragmenting) are not included.
"""

import socket
import base64
import secrets
import struct
import functools
import ssl
import urllib.parse
import re
import hashlib
import asyncio
from enum import IntEnum

GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


def xor_mask(data, mask):
    encoded = data.encode("utf-8")
    data_bytes = struct.unpack(f"{len(encoded)}c", encoded)
    return bytes(ord(byte) ^ mask[idx % 4] for idx, byte in enumerate(data_bytes))


class Status(IntEnum):
    NORMAL = 1000
    GOING_AWAY = 1001
    PROTOCOL_ERROR = 1002
    UNSUPPORTED_DATA_TYPE = 1003
    STATUS_NOT_AVAILABLE = 1005
    ABNORMAL_CLOSED = 1006
    INVALID_PAYLOAD = 1007
    POLICY_VIOLATION = 1008
    MESSAGE_TOO_BIG = 1009
    INVALID_EXTENSION = 1010
    UNEXPECTED_CONDITION = 1011
    SERVICE_RESTART = 1012
    TRY_AGAIN_LATER = 1013
    BAD_GATEWAY = 1014
    TLS_HANDSHAKE_ERROR = 1015


class Opcode(IntEnum):
    CONT = 0x0
    TEXT = 0x1
    BINARY = 0x2
    CLOSE = 0x8
    PING = 0x9
    PONG = 0xA


class WebsocketException(Exception):
    pass


class Frame:
    def __init__(self, length, data_start, opcode, fin, rsv1, rsv2, rsv3):
        self.length = length
        self.data_start = data_start
        self.opcode = opcode
        self.fin = fin
        self.rsv1 = rsv1
        self.rsv2 = rsv2
        self.rsv3 = rsv3

    @staticmethod
    def encode(data, opcode=Opcode.TEXT, masked=1):
        # https://datatracker.ietf.org/doc/html/rfc6455#section-5.2
        fin, rsv1, rsv2, rsv3 = 1, 0, 0, 0
        header = bytes([opcode | rsv3 << 4 | rsv2 << 5 | rsv1 << 6 | fin << 7])

        length = len(data)
        len_bytes = bytes(
            [
                (length if length <= 125 else 126 if length < 65536 else 127)
                | masked << 7
            ]
        )

        if length > 125:
            if length >= 65536:
                len_bytes += struct.pack("!Q", length)
            else:
                len_bytes += struct.pack("!H", length)

        if not masked:
            return header + len_bytes + data.encode("utf-8")

        mask = secrets.token_bytes(4)
        return header + len_bytes + mask + xor_mask(data, mask)

    @staticmethod
    def decode_beginning(response):
        header = response[0]
        fin, rsv1, rsv2, rsv3, opcode = (
            (header >> 7) & 1,
            (header >> 6) & 1,
            (header >> 5) & 1,
            (header >> 4) & 1,
            header & 0xF,
        )

        if response[1] >> 7:
            # If frames are masked close the connection
            return None, WebsocketException("Server frame was masked")

        data_start = 2
        length = response[1]
        if length > 125:
            if length == 126:
                data_start = 4
                length_bytes = response[2:4]
            elif length == 127:
                data_start = 10
                length_bytes = response[2:10]

            length = functools.reduce(
                lambda current, byte: (current << 8) | byte, length_bytes
            )

        return Frame(length, data_start, opcode, fin, rsv1, rsv2, rsv3), None


class Websocket:
    def __init__(self):
        self.connected = False

    def connect(self, url, headers={}):
        parsed_url = urllib.parse.urlparse(url)

        unsecure_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        secure = parsed_url.scheme == "wss"

        if secure:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            ssl_context.verify_mode = ssl.CERT_NONE
            self.sock = ssl_context.wrap_socket(
                unsecure_sock, server_hostname=parsed_url.hostname
            )
        else:
            self.sock = unsecure_sock

        self.sock.connect(
            (
                socket.gethostbyname(parsed_url.hostname),
                parsed_url.port or (443 if secure else 80),
            )
        )

        self.handshake(parsed_url, headers, secure)

    def handshake(self, parsed_url, headers, secure):
        ws_key = base64.b64encode(secrets.token_bytes(16)).decode("utf-8")

        # https://datatracker.ietf.org/doc/html/rfc6455#section-1.3
        default_headers = {
            "Host": parsed_url.hostname,
            "Upgrade": "websocket",
            "Connection": "Upgrade",
            "Sec-Websocket-Key": ws_key,
            "Sec-Websocket-Version": "13",
            "Origin": f"{'https' if secure else 'http'}://{parsed_url.netloc}",
        }
        handshake_headers = {**default_headers, **headers}

        handshake_str = "".join(
            f"{key}: {value}\r\n" for key, value in handshake_headers.items()
        )

        self.sock.sendall(
            f"GET {parsed_url.path or '/'} HTTP/1.1\r\n{handshake_str}\r\n".encode(
                "utf-8"
            )
        )
        response = self.sock.recv(1024).decode("utf-8")

        status_match = re.search("HTTP/\d\.\d 101", response)
        key_match = re.search("(?i:Sec-Websocket-Accept\: )(?P<key>.*)\r\n", response)

        if (
            not status_match
            or not key_match
            or key_match.groupdict()["key"]
            != base64.b64encode(
                hashlib.sha1((ws_key + GUID).encode("utf-8")).digest()
            ).decode("utf-8")
        ):
            self.sock.close()
            self.sock = None
            raise WebsocketException("Handshake failed")

        self.connected = True

    def send(self, data):
        if isinstance(data, bytes):
            self.sock.sendall(Frame.encode(data, Opcode.BINARY))
        else:
            self.sock.sendall(Frame.encode(data, Opcode.TEXT))

    def recv_data(self):
        beginning_data = self.sock.recv(10)
        frame, err = Frame.decode_beginning(beginning_data)
        if err:
            self.close(Status.PROTOCOL_ERROR, "Server frame was masked")
            raise err

        header_length = frame.data_start

        remaining_data = (
            self.sock.recv(frame.length - header_length)
            if frame.length + header_length > 10
            else b""
        )
        frame_data = beginning_data + remaining_data
        data = frame_data[frame.data_start : frame.data_start + frame.length]

        if frame.opcode == Opcode.CLOSE:
            code = int.from_bytes(data[:2], byteorder="big")
            self.close(code, data[2:].decode("utf-8"))
        elif frame.opcode == Opcode.PING:
            self.pong(data.decode("utf-8"))

        return (data, frame.opcode)

    def recv(self):
        while True:
            data, opcode = self.recv_data()
            if opcode == Opcode.BINARY:
                return data
            elif opcode == Opcode.TEXT:
                return data.decode("utf-8")

    def close(self, code=Status.NORMAL, reason=""):
        if not self.sock:
            return

        # https://datatracker.ietf.org/doc/html/rfc6455#section-1.4
        body = code.to_bytes(2, byteorder="big").decode("raw_unicode_escape") + reason
        self.sock.sendall(Frame.encode(body, Opcode.CLOSE))

        # The server probably should send a closing handshake
        # but it doesn't really matter what happens here
        self.sock.close()
        self.sock = None
        self.connected = False

    def ping(self, data=""):
        self.sock.sendall(Frame.encode(data, Opcode.PING))

    def pong(self, data=""):
        self.sock.sendall(Frame.encode(data, Opcode.PONG))


class AsyncWebsocket:
    def __init__(self):
        self.connected = False

    async def connect(self, url, headers={}):
        parsed_url = urllib.parse.urlparse(url)

        secure = parsed_url.scheme == "wss"

        self.reader, self.writer = await asyncio.open_connection(
            parsed_url.hostname, parsed_url.port or (443 if secure else 80), ssl=secure
        )

        await self.handshake(parsed_url, headers, secure)

    async def handshake(self, parsed_url, headers, secure):
        ws_key = base64.b64encode(secrets.token_bytes(16)).decode("utf-8")

        default_headers = {
            "Host": parsed_url.hostname,
            "Upgrade": "websocket",
            "Connection": "Upgrade",
            "Sec-Websocket-Key": ws_key,
            "Sec-Websocket-Version": "13",
            "Origin": f"{'https' if secure else 'http'}://{parsed_url.netloc}",
        }
        handshake_headers = {**default_headers, **headers}

        handshake_str = "".join(
            f"{key}: {value}\r\n" for key, value in handshake_headers.items()
        )

        self.writer.write(
            f"GET {parsed_url.path or '/'} HTTP/1.1\r\n{handshake_str}\r\n".encode(
                "utf-8"
            )
        )
        await self.writer.drain()

        response = (await self.reader.read(1024)).decode("utf-8")

        status_match = re.search("HTTP/\d\.\d 101", response)
        key_match = re.search("(?i:Sec-Websocket-Accept\: )(?P<key>.*)\r\n", response)

        if (
            not status_match
            or not key_match
            or key_match.groupdict()["key"]
            != base64.b64encode(
                hashlib.sha1((ws_key + GUID).encode("utf-8")).digest()
            ).decode("utf-8")
        ):
            self.writer.close()
            self.reader = self.writer = None
            raise WebsocketException("Handshake failed")

        self.connected = True

    async def send(self, data):
        if isinstance(data, bytes):
            self.writer.write(Frame.encode(data, Opcode.BINARY))
        else:
            self.writer.write(Frame.encode(data, Opcode.TEXT))

        await self.writer.drain()

    async def recv_data(self):
        beginning_data = await self.reader.read(10)
        frame, err = Frame.decode_beginning(beginning_data)
        if err:
            self.close(Status.PROTOCOL_ERROR, "Server frame was masked")
            raise err

        header_length = frame.data_start

        remaining_data = (
            await self.reader.read(frame.length - header_length)
            if frame.length + header_length > 10
            else b""
        )
        frame_data = beginning_data + remaining_data
        data = frame_data[frame.data_start : frame.data_start + frame.length]

        if frame.opcode == Opcode.CLOSE:
            code = int.from_bytes(data[:2], byteorder="big")
            await self.close(code, data[2:].decode("utf-8"))
        elif frame.opcode == Opcode.PING:
            await self.pong(data.decode("utf-8"))

        return (data, frame.opcode)

    async def recv(self):
        while True:
            data, opcode = await self.recv_data()
            if opcode == Opcode.BINARY:
                return data
            elif opcode == Opcode.TEXT:
                return data.decode("utf-8")

    async def close(self, code=Status.NORMAL, reason=""):
        if not self.writer:
            return

        body = code.to_bytes(2, byteorder="big").decode("raw_unicode_escape") + reason
        self.writer.write(Frame.encode(body, Opcode.CLOSE))
        await self.writer.drain()

        # The server probably should send a closing handshake but it doesn't really matter what happens here
        self.writer.close()
        self.reader = self.writer = None
        self.connected = False

    async def ping(self, data=""):
        self.writer.write(Frame.encode(data, Opcode.PING))
        await self.writer.drain()

    async def pong(self, data=""):
        self.writer.write(Frame.encode(data, Opcode.PONG))
        await self.writer.drain()
