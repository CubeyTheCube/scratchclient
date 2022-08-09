import requests

from .ScratchExceptions import *
from .util import get_data_list


class ProjectComment:
    def __init__(self, project, data, client):
        self.id = data["id"]
        self.parent_id = data["parent_id"]
        self.commentee_id = data["commentee_id"]
        self.content = data["content"]
        self.reply_count = data["reply_count"]

        self.author = data["author"]["username"]
        self.author_id = data["author"]["id"]

        self.created_timestamp = data["datetime_created"]
        self.last_modified_timestamp = data["datetime_modified"]

        self.visible = data["visibility"] == "visible"

        self.project = project
        self._client = client

    def delete(self):
        self._client._ensure_logged_in()

        if self._client.username != self.project.author.username:
            raise UnauthorizedException("You are not allowed to do that")

        requests.delete(
            f"https://api.scratch.mit.edu/proxy/comments/project/{self.project.id}/comment/{self.id}",
            headers=self.project._headers,
        )

    def report(self):
        self._client._ensure_logged_in()

        requests.post(
            f"https://api.scratch.mit.edu/proxy/comments/project/{self.project.id}/comment/{self.id}",
            headers=self.project._headers,
        )

    def reply(self, content):
        self._client._ensure_logged_in()

        if not self.project.comments_allowed:
            raise UnauthorizedException("Comments are closed on this project")

        return self.project.post_comment(content, self.id, self.author_id)

    def get_replies(self):
        return get_data_list(
            all,
            limit,
            offset,
            f"https://api.scratch.mit.edu/projects/{self.project_id}/comments/{self.id}/replies",
            lambda reply: ProjectComment(self.project, reply, self._client),
        )


class StudioComment:
    def __init__(self, studio, data, client):
        self.id = data["id"]
        self.parent_id = data["parent_id"]
        self.commentee_id = data["commentee_id"]
        self.content = data["content"]
        self.reply_count = data["reply_count"]

        self.author = data["author"]["username"]
        self.author_id = data["author"]["id"]

        self.created_timestamp = data["datetime_created"]
        self.last_modified_timestamp = data["datetime_modified"]

        self.visible = data["visibility"] == "visible"

        self.studio = studio
        self._client = client

    def delete(self):
        self._client._ensure_logged_in()

        response = requests.delete(
            f"https://api.scratch.mit.edu/proxy/comments/studio/{self.studio.id}/comment/{self.id}",
            headers=self.project._headers,
        )

        if response.status_code == 403:
            raise UnauthorizedException("You are not allowed to do that")

    def report(self):
        self._client._ensure_logged_in()

        requests.post(
            f"https://api.scratch.mit.edu/proxy/comments/studio/{self.studio.id}/comment/{self.id}",
            headers=self.project._headers,
        )

    def reply(self, content):
        self._client._ensure_logged_in()

        if not self.studio.comments_allowed:
            raise UnauthorizedException("Comments are closed on this studio")

        return self.studio.post_comment(content, self.id, self.author_id)

    def get_replies(self, all=False, limit=20, offset=0):
        return get_data_list(
            all,
            limit,
            offset,
            f"https://api.scratch.mit.edu/studios/{self.studio_id}/comments/{self.id}/replies",
            lambda reply: StudioComment(self.studio, reply, self._client),
        )


class ProfileComment:
    def __init__(self, data, client, user):
        self.id = data["id"]
        self.parent_id = data["parent_id"]
        self.commentee_id = data["commentee_id"]
        self.content = data["content"]
        self.replies = data["replies"]

        self.author = data["author"]["username"]
        self.author_id = data["author"]["id"]

        self.created_timestamp = data["datetime_created"]
        self.last_modified_timestamp = data["datetime_modified"]

        self.visible = data["visibility"] == "visible"

        self.user = user
        self._client = client

    def _comment_action(self, action, comment_id, user, client):
        client._ensure_logged_in()

        data = {
            "id": comment_id,
        }

        response = requests.post(
            f"https://scratch.mit.edu/site-api/comments/user/{user}/{action}/",
            headers=client._headers,
            data=json.dumps(data),
        )

        if response.status_code == 403:
            raise UnauthorizedException("You are not allowed to do that")

    def delete(self):
        self._comment_action("del", self.id, self.user, self._client)

    def report(self):
        self._comment_action("rep", self.id, self.user, self._client)

    def reply(self, content):
        self._client._ensure_logged_in()

        if not self.studio.comments_allowed:
            raise UnauthorizedException("Comments are closed on this profile")

        self._client.get_user(self.user).post_comment(
            content, self.id, self.author_id
        )
