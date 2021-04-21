import requests
import re
import json

from .ScratchExceptions import *
from .User import User
from .Project import Project
from .Studio import Studio
from .News import News
from .Message import Message
from .CloudConnection import CloudConnection
from .IncompleteUser import IncompleteUser
from .ProjectComment import ProjectComment


class ScratchSession:
    def __init__(self, username, password):
        self.username = username
        self.login(password)

    def login(self, password):
        # logs in to Scratch
        headers = {
            "x-csrftoken": "a",
            "x-requested-with": "XMLHttpRequest",
            "Cookie": "scratchcsrftoken=a;scratchlanguage=en;",
            "referer": "https://scratch.mit.edu",
        }
        data = json.dumps({"username": self.username, "password": password})

        request = requests.post(
            "https://scratch.mit.edu/login/", data=data, headers=headers
        )

        try:
            self.session_id = re.search('"(.*)"', request.headers["Set-Cookie"]).group()
            self.token = request.json()[0]["token"]
        except AttributeError:
            raise InvalidCredentialsException("Your password or username is incorrect")
        headers = {
            "x-requested-with": "XMLHttpRequest",
            "Cookie": "scratchlanguage=en;permissions=%7B%7D;",
            "referer": "https://scratch.mit.edu",
        }
        request = requests.get("https://scratch.mit.edu/csrf_token/", headers=headers)
        self.csrf_token = re.search(
            "scratchcsrftoken=(.*?);", request.headers["Set-Cookie"]
        ).group(1)
        self.user = self.get_user(self.username)

    # Internal functions to convert raw data to objects
    def _to_project(self, data):
        return Project(data, self)

    def _to_user(self, data):
        return User(data, self)

    def _to_studio(self, data):
        return Studio(data, self)

    def _to_news(self, data):
        return News(data)

    def _to_message(self, data):
        return Message(data)

    def get_user(self, user):
        username = user.username if isinstance(user, IncompleteUser) else user
        return self._to_user(
            requests.get("https://api.scratch.mit.edu/users/" + username + "/").json(),
        )

    def get_project(self, id):
        return self._to_project(
            requests.get(
                "https://api.scratch.mit.edu/projects/" + str(id) + "/"
            ).json(),
        )

    def get_studio(self, id):
        return self._to_studio(
            requests.get("https://api.scratch.mit.edu/studios/" + str(id) + "/").json(),
        )

    def get_news(self):
        return list(
            map(self._to_news, requests.get("https://api.scratch.mit.edu/news/").json())
        )

    def get_messages(self, all=False, limit=20, offset=0):
        headers = {
            "x-csrftoken": self.csrf_token,
            "X-Token": self.token,
            "x-requested-with": "XMLHttpRequest",
            "Cookie": "scratchcsrftoken="
            + self.csrf_token
            + ";scratchlanguage=en;scratchsessionsid="
            + self.session_id
            + ";",
            "referer": "https://scratch.mit.edu",
        }
        if all:
            messages = []
            offset = 0
            while True:
                res = requests.get(
                    "https://api.scratch.mit.edu/users/"
                    + self.username
                    + "/messages/"
                    + "?limit=40&offset="
                    + str(offset),
                    headers=headers,
                ).json()
                messages += res
                if len(res) != 40:
                    break
                offset += 40
            return list(map(self._to_message, studios))
        else:
            return list(
                map(
                    self._to_message,
                    requests.get(
                        "https://api.scratch.mit.edu/users/"
                        + self.username
                        + "/messages/"
                        + "?limit="
                        + str(limit)
                        + "&offset="
                        + str(offset),
                        headers=headers,
                    ).json(),
                )
            )

    def create_cloud_connection(self, project_id):
        return CloudConnection(project_id, self)

    def explore_projects(self, mode="trending", query="*"):
        return list(
            map(
                self._to_project,
                requests.get(
                    "https://api.scratch.mit.edu/explore/projects/?mode="
                    + mode
                    + "&q="
                    + query
                ).json(),
            )
        )

    def explore_studios(self, mode="trending", query="*"):
        return list(
            map(
                self._to_studio,
                requests.get(
                    "https://api.scratch.mit.edu/explore/studios/?mode="
                    + mode
                    + "&q="
                    + query
                ).json(),
            )
        )

    def search_projects(self, mode="popular", query="*"):
        return list(
            map(
                self._to_project,
                requests.get(
                    "https://api.scratch.mit.edu/search/projects/?mode="
                    + mode
                    + "&q="
                    + query
                ).json(),
            )
        )

    def search_studios(self, mode="popular", query="*"):
        return list(
            map(
                self._to_studio,
                requests.get(
                    "https://api.scratch.mit.edu/search/studios/?mode="
                    + mode
                    + "&q="
                    + query
                ).json(),
            )
        )
