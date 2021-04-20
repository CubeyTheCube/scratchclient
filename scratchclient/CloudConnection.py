import websocket
import json
import time
import numpy
import wsaccel
import threading
from pymitter import EventEmitter


class CloudVariable:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value


class CloudConnection(EventEmitter):
    def __init__(self, project_id, client):
        EventEmitter.__init__(self)
        self._client = client
        self.connect(project_id)

    def _send_packet(self, packet):
        self._ws.send(json.dumps(packet) + "\n")

    def connect(self, project_id):
        if project_id:
            self.project_id = project_id
        self._ws = websocket.WebSocket()
        self._cloudvariables = []
        self._timer = time.time()
        self._ws.connect(
            "wss://clouddata.scratch.mit.edu",
            cookie="scratchsessionsid=" + self._client.session_id + ";",
            origin="https://scratch.mit.edu",
            enable_multithread=True,
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
            except:
                pass
            else:
                self._cloudvariables.append(
                    CloudVariable(variable["name"], variable["value"])
                )
        self._start_cloud_var_loop()

    def set_cloud_variable(self, variable, value):
        if time.time() - self._timer > 0.1:
            if not str(value).isdigit():
                raise ValueError(
                    "Cloud variables can only be set to a combination of numbers"
                )
            try:
                packet = {
                    "method": "set",
                    "name": (
                        "☁ " + variable if not variable.startswith("☁ ") else variable
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
                        cloud.name == "☁ " + variable
                        if not variable.startswith("☁ ")
                        else variable
                    ):
                        cloud.value = value
                        self.emit("set", cloud)
                        break
            except (
                BrokenPipeError,
                websocket._exceptions.WebSocketConnectionClosedException,
            ):
                self.connect()
                time.sleep(0.1)
                self.set_cloud_variable(variable, value)
                return
        else:
            time.sleep(time.time() - self._timer)
            self.set_cloud_variable(variable, value)

    def _cloud_var_loop(self):
        while True:
            if self._ws.connected:
                response = self._ws.recv()
                response = json.loads(response)
                for cloud in self._cloudvariables:
                    if response["name"] == cloud.name:
                        cloud.value = response["value"]
                        self.cloud.emit("set", cloud)

            else:
                self.connect()

    def _start_cloud_var_loop(self):
        """Will start a new thread that looks for the cloud variables and appends their results onto cloudvariables"""
        thread = threading.Thread(target=self._cloud_var_loop)
        thread.start()

    def get_cloud_variable(self, name):
        try:
            var = next(
                x
                for x in self._cloudvariables
                if x.name == ("☁ " + name if not name.startswith("☁ ") else name)
            )
            return var.value
        except StopIteration:
            raise ValueError(
                "Variable '"
                + ("☁ " + name if not name.startswith("☁ ") else name)
                + "' is not in this project"
            )
