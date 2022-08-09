import requests


class BackpackItem:
    def __init__(self, data, client):
        self.body_URL = f"https://backpack.scratch.mit.edu/{data['body']}"
        self.thumbnail_URL = data["thumbnail"]
        self.id = data["id"]
        self.mime = data["mime"]
        self.name = data["name"]
        self.type = data["type"]

        self._client = client

    def delete(self):
        self._client._ensure_logged_in()

        requests.delete(
            f"https://backpack.scratch.mit.edu/{self._client.username}/{self.id}",
            headers=self._client._headers,
        )
