import json
import time
import threading
import asyncio

from .Websocket import Websocket, AsyncWebsocket
from .ScratchExceptions import *


class EventEmitter:
    def __init__(self):
        self._events = {}

    def on(self, key, callback=None, once=False):
        def add_handler(handler):
            if not key in self._events:
                self._events[key] = []

            self._events[key].append((handler, once))

        if callback:
            add_handler(callback)
            return

        return add_handler

    def off(self, key, callback):
        self._events[key] = [
            (handler, once)
            for handler, once in self._events[key]
            if handler is not callback
        ]

    def once(self, key, callback=None):
        return self.on(key, callback, True)

    def emit(self, key, *args, **kwargs):
        if not key in self._events:
            return

        for handler, once in self._events[key]:
            if asyncio.iscoroutinefunction(handler):
                asyncio.create_task(handler(*args, **kwargs))
            else:
                handler(*args, **kwargs)

            if once:
                self.off(key, handler)

    def listeners(self, event):
        return self._events[event][0]


class CloudVariable:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class BaseCloudConnection(EventEmitter):
    def __init__(self, project_id, client, cloud_host):
        super().__init__()
        self._client = client
        self.project_id = project_id
        self.cloud_host = cloud_host
        self._ws = None

    def _send_packet(self, packet):
        return self._ws.send(f"{json.dumps(packet)}\n")

    def get_cloud_variable(self, name):
        try:
            var = next(
                x
                for x in self._cloudvariables
                if x.name == (f"☁ {name}" if not name.startswith("☁ ") else name)
            )
            return var.value
        except StopIteration:
            raise CloudVariableException(
                f"Variable '{(f'☁ {name}' if not name.startswith('☁ ') else name)}' is not in this project"
            )


class CloudConnection(BaseCloudConnection):
    def __init__(
        self, project_id, client, cloud_host="clouddata.scratch.mit.edu", headers={}
    ):
        super().__init__(project_id, client, cloud_host)
        self.connect(headers)

    def connect(self, headers):
        self._ws = Websocket()
        self._cloudvariables = []
        self._timer = time.time()

        default_headers = {
            "Cookie": f"scratchsessionsid={self._client.session_id};",
            "Origin": "https://scratch.mit.edu",
        }
        if self.cloud_host == "clouddata.scratch.mit.edu":
            if not self._client.logged_in:
                raise UnauthorizedException("You need to be logged in to do this")
        else:
            # Don't send the session ID unless it's Scratch
            del default_headers["Cookie"]

        self._ws.connect(
            f"wss://{self.cloud_host}",
            headers={**default_headers, **headers},
        )  # connect the websocket
        self._send_packet(
            {
                "method": "handshake",
                "user": self._client.username,
                "project_id": str(self.project_id),
            }
        )
        self.emit("handshake")
        response = self._ws.recv().split("\n")
        for variable in response:
            try:
                variable = json.loads(str(variable))
            except json.decoder.JSONDecodeError:
                pass
            else:
                self._cloudvariables.append(
                    CloudVariable(variable["name"], variable["value"])
                )
        self.emit("connect")
        self._start_cloud_var_loop()

    def set_cloud_variable(self, variable, value):
        if time.time() - self._timer > 0.1:
            if not str(value).isdigit():
                raise CloudVariableException(
                    "Cloud variables can only be set to a combination of numbers"
                )

            if len(str(value)) > 256:
                raise CloudVariableException(
                    "Cloud variable values must be less than 256 characters long"
                )

            packet = {
                "method": "set",
                "name": (
                    f"☁ {variable}" if not variable.startswith("☁ ") else variable
                ),
                "value": str(value),
                "user": self._client.username,
                "project_id": str(self.project_id),
            }
            self._send_packet(packet)
            self.emit("outgoing", packet)
            self._timer = time.time()
            for cloud in self._cloudvariables:
                if (
                    cloud.name == f"☁ {variable}"
                    if not variable.startswith("☁ ")
                    else variable
                ):
                    cloud.value = value
                    self.emit("change", cloud)
                    break
        else:
            time.sleep(time.time() - self._timer)
            self.set_cloud_variable(variable, value)

    def create_cloud_variable(self, name, initial_value=0):
        if time.time() - self._timer > 0.1:
            if not str(initial_value).isdigit():
                raise CloudVariableException(
                    "Cloud variables can only be set to a combination of numbers"
                )

            if len(str(initial_value)) > 256:
                raise CloudVariableException(
                    "Cloud variable values must be less than 256 characters long"
                )

            packet = {
                "method": "create",
                "name": (f"☁ {name}" if not name.startswith("☁ ") else name),
                "value": str(initial_value),
                "user": self._client.username,
                "project_id": str(self.project_id),
            }
            self._send_packet(packet)
            self.emit("outgoing", packet)
            self._timer = time.time()

            new_variable = CloudVariable(f"☁ {name}" if not name.startswith("☁ ") else name, str(initial_value))
            self._cloudvariables.append(new_variable)
            self.emit("create", new_variable)
            self.emit("change", new_variable)
        else:
            time.sleep(time.time() - self._timer)
            self.create_cloud_variable(name, initial_value)

    def delete_cloud_variable(self, name):
        if time.time() - self._timer > 0.1:
            packet = {
                "method": "delete",
                "name": (f"☁ {name}" if not name.startswith("☁ ") else name),
                "user": self._client.username,
                "project_id": str(self.project_id),
            }
            self._send_packet(packet)
            self.emit("outgoing", packet)
            self._timer = time.time()

            self.emit("delete", name)
        else:
            time.sleep(time.time() - self._timer)
            self.delete_cloud_variable(name)

    def _cloud_var_loop(self):
        while True:
            if self._ws.connected:
                response = self._ws.recv()
                response = json.loads(response)

                if response["method"] != "set":
                    continue

                try:
                    cloud = next(
                        variable
                        for variable in self._cloudvariables
                        if response["name"] == variable.name
                    )
                    cloud.value = response["value"]
                except StopIteration:
                    # A new variable was created and was set
                    cloud = CloudVariable(response["name"], response["value"])
                    self._cloudvariables.append(cloud)
                    self.emit("create", cloud)

                self.emit("set", cloud)
                self.emit("change", cloud)
            else:
                self.connect()

    def _start_cloud_var_loop(self):
        """Will start a new thread that looks for the cloud variables and appends their results onto cloudvariables"""
        thread = threading.Thread(target=self._cloud_var_loop)
        thread.start()


class AsyncCloudConnection(BaseCloudConnection):
    def __init__(
        self, project_id, client, cloud_host="clouddata.scratch.mit.edu", headers={}
    ):
        super().__init__(project_id, client, cloud_host)
        self._headers = headers

    def run(self):
        asyncio.run(self.connect())

    async def connect(self):
        self._ws = AsyncWebsocket()
        self._cloudvariables = []
        self._timer = time.time()

        default_headers = {
            "Cookie": f"scratchsessionsid={self._client.session_id};",
            "Origin": "https://scratch.mit.edu",
        }
        if self.cloud_host == "clouddata.scratch.mit.edu":
            if not self._client.logged_in:
                raise UnauthorizedException("You need to be logged in to do this")
        else:
            # Don't send the session ID unless it's Scratch
            del default_headers["Cookie"]

        await self._ws.connect(
            f"wss://{self.cloud_host}",
            headers={**default_headers, **self._headers},
        )  # connect the websocket

        await self._send_packet(
            {
                "method": "handshake",
                "user": self._client.username,
                "project_id": str(self.project_id),
            }
        )
        self.emit("handshake")
        response = (await self._ws.recv()).split("\n")
        for variable in response:
            try:
                variable = json.loads(str(variable))
            except json.decoder.JSONDecodeError:
                pass
            else:
                self._cloudvariables.append(
                    CloudVariable(variable["name"], variable["value"])
                )
        self.emit("connect")

        await self.cloud_variable_loop()

    async def set_cloud_variable(self, variable, value):
        if time.time() - self._timer > 0.1:
            if not str(value).isdigit():
                raise CloudVariableException(
                    "Cloud variables can only be set to a combination of numbers"
                )

            if len(str(value)) > 256:
                raise CloudVariableException(
                    "Cloud variable values must be less than 256 characters long"
                )

            packet = {
                "method": "set",
                "name": (
                    f"☁ {variable}" if not variable.startswith("☁ ") else variable
                ),
                "value": str(value),
                "user": self._client.username,
                "project_id": str(self.project_id),
            }
            await self._send_packet(packet)
            self.emit("outgoing", packet)
            self._timer = time.time()
            for cloud in self._cloudvariables:
                if (
                    cloud.name == f"☁ {variable}"
                    if not variable.startswith("☁ ")
                    else variable
                ):
                    cloud.value = value
                    self.emit("change", cloud)
                    break
        else:
            await asyncio.sleep(time.time() - self._timer)
            await self.set_cloud_variable(variable, value)

    async def create_cloud_variable(self, name, initial_value=0):
        if time.time() - self._timer > 0.1:
            if not str(initial_value).isdigit():
                raise CloudVariableException(
                    "Cloud variables can only be set to a combination of numbers"
                )

            if len(str(initial_value)) > 256:
                raise CloudVariableException(
                    "Cloud variable values must be less than 256 characters long"
                )

            packet = {
                "method": "create",
                "name": (f"☁ {name}" if not name.startswith("☁ ") else name),
                "value": str(initial_value),
                "user": self._client.username,
                "project_id": str(self.project_id),
            }
            await self._send_packet(packet)
            self.emit("outgoing", packet)
            self._timer = time.time()

            new_variable = CloudVariable(f"☁ {name}" if not name.startswith("☁ ") else name, str(initial_value))
            self._cloudvariables.append(new_variable)
            self.emit("create", new_variable)
            self.emit("change", new_variable)
        else:
            await asyncio.sleep(time.time() - self._timer)
            await self.create_cloud_variable(name, initial_value)

    async def delete_cloud_variable(self, name):
        if time.time() - self._timer > 0.1:
            packet = {
                "method": "delete",
                "name": (f"☁ {name}" if not name.startswith("☁ ") else name),
                "user": self._client.username,
                "project_id": str(self.project_id),
            }
            await self._send_packet(packet)
            self.emit("outgoing", packet)
            self._timer = time.time()

            self.emit("delete", name)
        else:
            await asyncio.sleep(time.time() - self._timer)
            await self.delete_cloud_variable(name)

    async def cloud_variable_loop(self):
        while True:
            if self._ws.connected:
                response = await self._ws.recv()
                response = json.loads(response)

                if response["method"] != "set":
                    continue

                try:
                    cloud = next(
                        variable
                        for variable in self._cloudvariables
                        if response["name"] == variable.name
                    )
                    cloud.value = response["value"]
                except StopIteration:
                    # A new variable was created and was set
                    cloud = CloudVariable(response["name"], response["value"])
                    self._cloudvariables.append(cloud)
                    self.emit("create", cloud)

                self.emit("set", cloud)
                self.emit("change", cloud)
            else:
                await self.connect()
