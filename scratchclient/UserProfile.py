import requests
import json
import pathlib

from .Project import Project
from .Incomplete import IncompleteProject, RemixtreeProject

class UserProfile:
    def __init__(self, data, user):
        self.user = user
        self._client = user._client
        self.username = user.username
        self.id = data["id"]
        self.avatar_URL = data["images"]["90x90"]
        self.bio = data["bio"]
        self.status = data["status"]
        self.country = data["country"]

    def set_bio(self, content):
        self._client._ensure_logged_in()

        if self.username != self._client.username:
            raise UnauthorizedException("You are not allowed to do that")

        data = {"bio": content}

        requests.put(
            f"https://scratch.mit.edu/site-api/users/all/{self.username}/",
            data=json.dumps(data),
            headers=self.user._headers,
        )

        self.bio = content

    def set_status(self, content):
        self._client._ensure_logged_in()

        if self.username != self._client.username:
            raise UnauthorizedException("You are not allowed to do that")

        data = {"status": content}

        requests.put(
            f"https://scratch.mit.edu/site-api/users/all/{self.username}/",
            data=json.dumps(data),
            headers=self.user._headers,
        )

        self.status = content

    def set_avatar(self, filename):
        self._client._ensure_logged_in()

        if self.username != self._client.username:
            raise UnauthorizedException("You are not allowed to do that")

        files = {
            "file": (
                filename,
                open(filename, "rb"),
                f"image/{pathlib.Path(filename).suffix}",
            ),
        }

        requests.post(
            f"https://scratch.mit.edu/site-api/users/all/{self.username}/",
            files=files,
            headers=self.user._headers,
        )

    def get_featured_project(self):
        data = requests.get(
            f"https://scratch.mit.edu/site-api/users/all/{self.username}/",
        ).json()

        return IncompleteProject(data["featured_project_data"])

    def set_featured_project(self, label, project):
        self._client._ensure_logged_in()

        if self.username != self._client.username:
            raise UnauthorizedException("You are not allowed to do that")

        label_num = (
            {
                "featured_project": "",
                "featured_tutorial": 0,
                "work_in_progress": 1,
                "remix_this": 2,
                "my_favorite_things": 3,
                "why_i_scratch": 4,
            }
        )[label]
        project_id = project.id if isinstance(project, (Project, IncompleteProject, RemixtreeProject)) else project
        data = {"featured_project": project_id, "featured_project_label": label_num}

        requests.put(
            f"https://scratch.mit.edu/site-api/users/all/{self.username}/",
            data=json.dumps(data),
            headers=self._headers,
        )
