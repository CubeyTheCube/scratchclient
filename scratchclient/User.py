import requests
import json

from .ScratchExceptions import UnauthorizedException
from .UserProfile import *
from .Comment import ProjectComment
from .util import get_data_list


class User:
    def __init__(self, data, client):
        global Project
        global Studio
        from .Project import Project
        from .Studio import Studio

        self._client = client

        self.id = data["id"]
        self.username = data["username"]
        self.joined_timestamp = data["history"]["joined"]
        self.scratchteam = data["scratchteam"]
        self.profile = UserProfile(data["profile"], self)
        self._headers = {
            "x-csrftoken": self._client.csrf_token,
            "X-Token": self._client.token,
            "x-requested-with": "XMLHttpRequest",
            "Cookie": f"scratchcsrftoken={self._client.csrf_token};scratchlanguage=en;scratchsessionsid={self._client.session_id};",
            "referer": f"https://scratch.mit.edu/users/{self.username}/",
        }

    def get_projects(self, all=False, limit=20, offset=0):
        return get_data_list(
            all,
            limit,
            offset,
            f"https://api.scratch.mit.edu/users/{self.username}/projects",
            lambda project: Project(
                {**project, "author": {**project["author"], "username": self.username}},
                self._client,
            ),
        )

    def get_curating(self, all=False, limit=20, offset=0):
        return get_data_list(
            all,
            limit,
            offset,
            f"https://api.scratch.mit.edu/users/{self.username}/studios/curate",
            lambda studio: Studio(studio, self._client),
        )

    def get_favorites(self, all=False, limit=20, offset=0):
        return get_data_list(
            all,
            limit,
            offset,
            f"https://api.scratch.mit.edu/users/{self.username}/favorites",
            lambda project: Project(project, self._client),
        )

    def get_followers(self, all=False, limit=20, offset=0):
        return get_data_list(
            all,
            limit,
            offset,
            f"https://api.scratch.mit.edu/users/{self.username}/followers",
            lambda follower: User(follower, self._client),
        )

    def get_following(self, all=False, limit=20, offset=0):
        return get_data_list(
            all,
            limit,
            offset,
            f"https://api.scratch.mit.edu/users/{self.username}/following",
            lambda follower: User(follower, self._client),
        )

    def get_message_count(self):
        return requests.get(
            f"https://api.scratch.mit.edu/users/{self.username}/messages/count/",
            headers={
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
            },
        ).json()["count"]

    def post_comment(self, content, parent_id="", commentee_id=""):
        self._client._ensure_logged_in()

        data = {
            "commentee_id": commentee_id,
            "content": content,
            "parent_id": parent_id,
        }
        response = requests.post(
            f"https://scratch.mit.edu/site-api/comments/user/{self.username}/add",
            headers=self._headers,
            data=json.dumps(data),
        )

        if response.status_code == 403:
            raise UnauthorizedException("You are not allowed to do that")

    def delete_comment(self, comment_id):
        return ProjectComment._comment_action(
            None, "del", comment_id, self.username, self._client
        )

    def report_comment(self, comment_id):
        return ProjectComment._comment_action(
            None, "rep", comment_id, self.username, self._client
        )

    def report(self, field):
        self._client._ensure_logged_in()

        data = {"selected_field": field}
        requests.post(
            f"https://scratch.mit.edu/site-api/users/all/{self.username}/report",
            headers=self._headers,
            data=json.dumps(data),
        )

    def toggle_commenting(self):
        self._client._ensure_logged_in()

        if self.username != self._client.username:
            raise UnauthorizedException("You are not allowed to do that")

        requests.post(
            f"https://scratch.mit.edu/site-api/comments/user/{self.username}/toggle-comments/",
            headers=self._headers,
        )

    def follow(self):
        self._client._ensure_logged_in()

        return requests.put(
            f"https://scratch.mit.edu/site-api/users/followers/{self.username}/add/?usernames={self._client.username}",
            headers=self._headers,
        ).json()

    def unfollow(self):
        self._client._ensure_logged_in()

        return requests.put(
            f"https://scratch.mit.edu/site-api/users/followers/{self.username}/remove/?usernames={self._client.username}",
            headers=self._headers,
        ).json()
