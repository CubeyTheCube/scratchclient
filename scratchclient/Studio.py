import requests
import json

from .User import User
from .Project import Project


class Studio:
    def __init__(self, data, client):
        self.id = data["id"]
        self.title = data["title"]
        self.owner = data["owner"]
        self.description = data["description"]
        self.thumbnail_URL = data["image"]
        self.visible = data["visibility"] == "visibile"
        self.open_to_public = data["open_to_all"]

        self.created_timestamp = data["history"]["created"]
        self.last_modified_timestamp = data["history"]["modified"]

        self.follower_count = data["stats"]["followers"]

        self._client = client
        self._headers = {
            "x-csrftoken": self._client.csrf_token,
            "X-Token": self._client.token,
            "x-requested-with": "XMLHttpRequest",
            "Cookie": "scratchcsrftoken="
            + self._client.csrf_token
            + ";scratchlanguage=en;scratchsessionsid="
            + self._client.session_id
            + ";",
            "referer": "https://scratch.mit.edu/studios/" + str(self.id) + "/",
        }

    def add_project(self, project):
        project_id = project.id if isinstance(project, Project) else project
        headers = self._headers
        headers["referer"] = "https://scratch.mit.edu/projects/" + str(project_id) + "/"
        requests.post(
            "https://api.scratch.mit.edu/studios/"
            + str(self.id)
            + "/project/"
            + project_id
            + "/",
            headers=headers,
        )

    def remove_project(self, project):
        project_id = project.id if isinstance(project, Project) else project
        headers = self._headers
        headers["referer"] = "https://scratch.mit.edu/projects/" + str(project_id) + "/"
        requests.post(
            "https://api.scratch.mit.edu/studios/"
            + str(self.id)
            + "/project/"
            + project_id
            + "/",
            headers=headers,
        )

    def open_to_public(self):
        requests.put(
            "https://scratch.mit.edu/site-api/galleries/"
            + str(self.id)
            + "/mark/open/",
            headers=self._headers,
        )

    def close_to_public(self):
        requests.put(
            "https://scratch.mit.edu/site-api/galleries/"
            + str(self.id)
            + "/mark/closed/",
            headers=self._headers,
        )

    def follow(self):
        return requests.put(
            "https://scratch.mit.edu/site-api/users/bookmarkers/"
            + str(self.id)
            + "/add/?usernames="
            + self._client.username,
            headers=self._headers,
        ).json()

    def unfollow(self):
        return requests.put(
            "https://scratch.mit.edu/site-api/users/bookmarkers/"
            + str(self.id)
            + "/remove/?usernames="
            + self._client.username,
            headers=self._headers,
        ).json()

    def toggle_commenting(self):
        headers = self._headers
        headers["referer"] = (
            "https://scratch.mit.edu/studios/" + str(self.id) + "/comments/"
        )
        requests.post(
            "https://scratch.mit.edu/site-api/comments/gallery/"
            + str(self.id)
            + "/toggle-comments/",
            headers=headers,
        )

    def post_comment(self, content, parent_id="", commentee_id=""):
        headers = self._headers
        headers["referer"] = (
            "https://scratch.mit.edu/studios/" + str(self.id) + "/comments/"
        )
        data = {
            "commentee_id": commentee_id,
            "content": content,
            "parent_id": parent_id,
        }
        requests.post(
            "https://scratch.mit.edu/site-api/comments/gallery/"
            + str(self.id)
            + "/add/",
            headers=headers,
            data=json.dumps(data),
        )

    def delete_comment(self, comment_id):
        headers = self._headers
        headers["referer"] = (
            "https://scratch.mit.edu/studios/" + str(self.id) + "/comments/"
        )
        data = {"id": comment_id}
        requests.post(
            "https://scratch.mit.edu/site-api/comments/user/" + self.username + "/del/",
            headers=headers,
            data=json.dumps(data),
        )

    def report_comment(self, comment_id):
        headers = self._headers
        headers["referer"] = (
            "https://scratch.mit.edu/studios/" + str(self.id) + "/comments/"
        )
        data = {"id": comment_id}
        requests.post(
            "https://scratch.mit.edu/site-api/comments/user/" + self.username + "/rep/",
            headers=headers,
            data=json.dumps(data),
        )

    def invite_curator(self, user):
        username = user.username if isinstance(user, User) == str else user
        headers = self._headers
        headers["referer"] = (
            "https://scratch.mit.edu/studios/" + str(self.id) + "/curators/"
        )
        requests.put(
            "https://scratch.mit.edu/site-api/users/curators-in/"
            + str(self.id)
            + "/invite_curator/?usernames="
            + username,
            headers=headers,
        )

    def accept_curator(self):
        headers = self._headers
        headers["referer"] = (
            "https://scratch.mit.edu/studios/" + str(self.id) + "/curators/"
        )
        requests.put(
            "https://scratch.mit.edu/site-api/users/curators-in/"
            + str(self.id)
            + "/add/?usernames="
            + self._client.username,
            headers=headers,
        )

    def promote_curator(self, user):
        username = user.username if isinstance(user, User) == str else user
        headers = self._headers
        headers["referer"] = (
            "https://scratch.mit.edu/studios/" + str(self.id) + "/curators/"
        )
        requests.put(
            "https://scratch.mit.edu/site-api/users/curators-in/"
            + str(self.id)
            + "/promote/?usernames="
            + username,
            headers=headers,
        )

    def set_description(self, content):
        data = {"description": content}
        requests.put(
            "https://scratch.mit.edu/site-api/galleries/all/" + str(self.id) + "/",
            headers=self._headers,
            data=json.dumps(data),
        )
        self.description = content

    def set_title(self, content):
        data = {"title": content}
        requests.put(
            "https://scratch.mit.edu/site-api/galleries/all/" + str(self.id) + "/",
            headers=self._headers,
            data=json.dumps(data),
        )
        self.title = content
