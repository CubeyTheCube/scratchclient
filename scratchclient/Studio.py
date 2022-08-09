import requests
import json

from .Comment import StudioComment
from .Activity import Activity
from .Incomplete import IncompleteProject
from .ScratchExceptions import *
from .util import get_data_list


class Studio:
    def __init__(self, data, client):
        global User
        global Project
        from .User import User
        from .Project import Project

        self.id = data["id"]
        self.title = data["title"]
        # Backwards compatibility
        self.host = self.owner = data["host"]
        self.description = data["description"] if "description" in data else None
        self.thumbnail_URL = data["image"]
        self.visible = data["visibility"] == "visibile"
        self.open_to_public = data["open_to_all"]
        self.comments_allowed = data["comments_allowed"]

        self.created_timestamp = data["history"]["created"]
        self.last_modified_timestamp = data["history"]["modified"]

        self.curator_count = None
        if data["stats"]:
            if "curators" in data["stats"]:
                self.follower_count = None
                self.manager_count = None
                self.curator_count = data["stats"]["curators"]
            else:
                self.follower_count = data["stats"]["followers"]
                self.manager_count = data["stats"]["managers"]

            self.comment_count = data["stats"]["comments"]
            self.project_count = data["stats"]["projects"]
        else:
            self.follower_count = None
            self.comment_count = None
            self.manager_count = None
            self.project_count = None

        self._client = client
        self._headers = {
            "x-csrftoken": self._client.csrf_token,
            "X-Token": self._client.token,
            "x-requested-with": "XMLHttpRequest",
            "Cookie": f"scratchcsrftoken={self._client.csrf_token};scratchlanguage=en;scratchsessionsid={self._client.session_id};",
            "referer": f"https://scratch.mit.edu/studios/{self.id}/",
        }

    def add_project(self, project):
        self._client._ensure_logged_in()

        project_id = project if isinstance(project, (str, int)) else project.id
        headers = self._headers
        headers["referer"] = f"https://scratch.mit.edu/projects/{project_id}/"

        response = requests.post(
            f"https://api.scratch.mit.edu/studios/{self.id}/project/{project_id}/",
            headers=headers,
        )

        if response.status_code == 403:
            raise UnauthorizedException("You are not allowed to do this")

    def remove_project(self, project):
        self._client._ensure_logged_in()

        project_id = project if isinstance(project, (str, int)) else project.id
        headers = self._headers.copy()
        headers["referer"] = f"https://scratch.mit.edu/projects/{project_id}/"

        response = requests.delete(
            f"https://api.scratch.mit.edu/studios/{self.id}/project/{project_id}/",
            headers=headers,
        )

        if response.status_code == 403:
            raise UnauthorizedException("You are not allowed to do this")

    def get_projects(self, all=False, limit=20, offset=0):
        return get_data_list(
            all,
            limit,
            offset,
            f"https://api.scratch.mit.edu/studios/{self.id}/projects",
            lambda project: IncompleteProject(project),
        )

    def get_curators(self, all=False, limit=20, offset=0):
        return get_data_list(
            all,
            limit,
            offset,
            f"https://api.scratch.mit.edu/studios/{self.id}/curators",
            lambda curator: User(curator, self._client),
        )

    def get_managers(self, all=False, limit=20, offset=0):
        return get_data_list(
            all,
            limit,
            offset,
            f"https://api.scratch.mit.edu/studios/{self.id}/managers",
            lambda manager: User(manager, self._client),
        )

    def get_roles(self):
        self._client._ensure_logged_in()

        return requests.get(
            f"https://api.scratch.mit.edu/studios/{self.id}/users/{self._client.username}"
        ).json()

    def follow(self):
        self._client._ensure_logged_in()

        return requests.put(
            f"https://scratch.mit.edu/site-api/users/bookmarkers/{self.id}/add/?usernames={self._client.username}",
            headers=self._headers,
        ).json()

    def unfollow(self):
        self._client._ensure_logged_in()

        return requests.put(
            f"https://scratch.mit.edu/site-api/users/bookmarkers/{self.id}/remove/?usernames={self._client.username}",
            headers=self._headers,
        ).json()

    def open_to_public(self):
        self._client._ensure_logged_in()

        response = requests.put(
            f"https://scratch.mit.edu/site-api/galleries/{self.id}/mark/open/",
            headers=self._headers,
        )

        if response.status_code == 403:
            raise UnauthorizedException("You are not allowed to do this")

    def close_to_public(self):
        self._client._ensure_logged_in()

        response = requests.put(
            f"https://scratch.mit.edu/site-api/galleries/{self.id}/mark/open/",
            headers=self._headers,
        )

        if response.status_code == 403:
            raise UnauthorizedException("You are not allowed to do this")

    def toggle_commenting(self):
        self._client._ensure_logged_in()

        headers = self._headers.copy()
        headers["referer"] = f"https://scratch.mit.edu/studios/{self.id}/comments/"

        response = requests.post(
            f"https://scratch.mit.edu/site-api/comments/gallery/{self.id}/toggle-comments/",
            headers=headers,
        )

        if response.status_code == 403:
            raise UnauthorizedException("You are not allowed to do this")

    def get_comment(self, comment_id):
        data = requests.get(
            f"https://api.scratch.mit.edu/studios/{self.id}/comments/{comment_id}/"
        ).json()
        return StudioComment(self, data, self._client)

    def get_comments(self, all=False, limit=20, offset=0):
        return get_data_list(
            all,
            limit,
            offset,
            f"https://api.scratch.mit.edu/studios/{self.id}/comments",
            lambda comment: StudioComment(self, comment, self._client),
        )

    def get_activity(self, all=False, limit=20, offset=0):
        return get_data_list(
            all,
            limit,
            offset,
            f"https://api.scratch.mit.edu/studios/{self.id}/activity",
            Activity,
        )

    def post_comment(self, content, parent_id="", commentee_id=""):
        self._client._ensure_logged_in()

        if not self.comments_allowed:
            raise UnauthorizedException("Comments are closed in this studio")

        headers = self._headers.copy()
        headers["referer"] = f"https://scratch.mit.edu/studios/{self.id}/comments/"
        data = {
            "commentee_id": commentee_id,
            "content": content,
            "parent_id": parent_id,
        }

        response = requests.post(
            f"https://scratch.mit.edu/site-api/comments/gallery/{self.id}/add/",
            headers=headers,
            data=json.dumps(data),
        ).json()

        if "rejected" in response:
            raise RejectedException("Your comment did not post")

        return StudioComment(self, response, self._client)

    def delete_comment(self, comment_id):
        self._client._ensure_logged_in()

        headers = self._headers.copy()
        headers["referer"] = f"https://scratch.mit.edu/studios/{self.id}/comments/"
        data = {"id": comment_id}

        response = requests.post(
            f"https://scratch.mit.edu/site-api/comments/gallery/{self.id}/del/",
            headers=headers,
            data=json.dumps(data),
        )

        if response.status_code == 403:
            raise UnauthorizedException("You are not allowed to do this")

    def report_comment(self, comment_id):
        self._client._ensure_logged_in()

        headers = self._headers.copy()
        headers["referer"] = f"https://scratch.mit.edu/studios/{self.id}/comments/"

        data = {"id": comment_id}
        requests.post(
            f"https://scratch.mit.edu/site-api/comments/gallery/{self.id}/rep/",
            headers=headers,
            data=json.dumps(data),
        )

    def invite_curator(self, user):
        self._client._ensure_logged_in()

        username = user if isinstance(user, str) else user.username
        headers = self._headers.copy()
        headers["referer"] = f"https://scratch.mit.edu/studios/{self.id}/curators/"

        response = requests.put(
            f"https://scratch.mit.edu/site-api/users/curators-in/{self.id}/invite_curator/?usernames={username}",
            headers=headers,
        )

        if response.status_code == 403:
            raise UnauthorizedException("You are not allowed to do this")

    def accept_curator(self):
        self._client._ensure_logged_in()

        username = username = user if isinstance(user, str) else user.username
        headers = self._headers.copy()
        headers["referer"] = f"https://scratch.mit.edu/studios/{self.id}/curators/"

        response = requests.put(
            f"https://scratch.mit.edu/site-api/users/curators-in/{self.id}/add/?usernames={username}",
            headers=headers,
        )

        if response.status_code == 403:
            raise UnauthorizedException("You are not allowed to do this")

    def promote_curator(self, user):
        self._client._ensure_logged_in()

        username = username = user if isinstance(user, str) else user.username
        headers = self._headers.copy()
        headers["referer"] = f"https://scratch.mit.edu/studios/{self.id}/curators/"

        response = requests.put(
            f"https://scratch.mit.edu/site-api/users/curators-in/{self.id}/promote/?usernames={username}",
            headers=headers,
        )

        if response.status_code == 403:
            raise UnauthorizedException("You are not allowed to do this")

    def transfer_host(self, user, password):
        self._client._ensure_logged_in()

        username = username = user if isinstance(user, str) else user.username
        body = {"password": password}

        response = requests.put(
            f"https://api.scratch.mit.edu/studios/{self.id}/transfer/{username}",
            headers=self._headers,
            body=body,
        )

        if response.status_code == 403:
            raise UnauthorizedException("You are not allowed to do this")

    def set_description(self, content):
        self._client._ensure_logged_in()

        if self.host != self._client.user.id:
            raise UnauthorizedException("You are not allowed to do this")

        data = {"description": content}
        requests.put(
            f"https://scratch.mit.edu/site-api/galleries/all/{self.id}/",
            headers=self._headers,
            data=json.dumps(data),
        )
        self.description = content

    def set_title(self, content):
        self._client._ensure_logged_in()

        if self.host != self._client.user.id:
            raise UnauthorizedException("You are not allowed to do this")

        data = {"title": content}
        requests.put(
            f"https://scratch.mit.edu/site-api/galleries/all/{self.id}/",
            headers=self._headers,
            data=json.dumps(data),
        )
        self.title = content

    def set_thumbnail(self, file_or_data):
        self._client._ensure_logged_in()

        if self.host != self._client.user.id:
            raise UnauthorizedException("You are not allowed to do this")

        data = (
            file_or_data
            if isinstance(file_or_data, bytes)
            else open(file_or_data, "rb").read()
        )
        requests.post(
            f"https://scratch.mit.edu/site-api/galleries/all/{self.id}",
            data=data,
            headers=self._headers,
        )

    def delete(self):
        self._client._ensure_logged_in()

        if self.host != self._client.user.id:
            raise UnauthorizedException("You are not allowed to do that")

        data = {"visibility": "delbyusr"}

        requests.put(
            f"https://scratch.mit.edu/site-api/galleries/all/{self.id}/",
            data=json.dumps(data),
            headers=self._json_headers,
        )
