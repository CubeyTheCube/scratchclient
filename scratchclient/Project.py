import requests
import json

from .Incomplete import IncompleteUser, RemixtreeProject
from .ScratchExceptions import UnauthorizedException
from .Comment import ProjectComment
from .util import get_data_list


class Project:
    def __init__(self, data, client):
        global Studio
        from .Studio import Studio

        self.id = data["id"]
        self.title = data["title"]

        self.description = data["description"] if "description" in data else None
        self.instructions = data["instructions"] if "instructions" in data else None

        self.visible = data["visibility"] == "visible"
        self.public = data["public"]
        self.comments_allowed = data["comments_allowed"]
        self.is_published = data["is_published"]
        self.author = IncompleteUser(data["author"])
        self.thumbnail_URL = data["image"]

        self.created_timestamp = data["history"]["created"]
        self.last_modified_timestamp = data["history"]["modified"]
        self.shared_timestamp = data["history"]["shared"]

        self.view_count = data["stats"]["views"]
        self.love_count = data["stats"]["loves"]
        self.favorite_count = data["stats"]["favorites"]
        self.remix_count = data["stats"]["remixes"]

        if "remix" in data:
            self.parent = data["remix"]["parent"]
            self.root = data["remix"]["root"]
            self.is_remix = bool(self.parent)
        else:
            self.parent = None
            self.root = None
            self.is_remix = None

        self._client = client
        self._headers = {
            "x-csrftoken": self._client.csrf_token,
            "X-Token": self._client.token,
            "x-requested-with": "XMLHttpRequest",
            "Cookie": f"scratchcsrftoken={self._client.csrf_token};scratchlanguage=en;scratchsessionsid={self._client.session_id};",
            "referer": f"https://scratch.mit.edu/projects/{self.id}/",
        }
        self._json_headers = {
            **self._headers,
            "accept": "application/json",
            "Content-Type": "application/json",
        }

    def get_comment(self, comment_id):
        data = requests.get(
            f"https://api.scratch.mit.edu/users/{self.author.username}/projects/{self.id}/comments/{comment_id}/"
        ).json()
        return ProjectComment(self, data, self._client)

    def love(self):
        self._client._ensure_logged_in()

        return requests.post(
            f"https://api.scratch.mit.edu/proxy/projects/{self.id}/loves/user/{self._client.username}",
            headers=self._headers,
        ).json()["userLove"]

    def unlove(self):
        self._client._ensure_logged_in()

        return requests.delete(
            f"https://api.scratch.mit.edu/proxy/projects/{self.id}/loves/user/{self._client.username}",
            headers=self._headers,
        ).json()["userLove"]

    def favorite(self):
        self._client._ensure_logged_in()

        return requests.post(
            f"https://api.scratch.mit.edu/proxy/projects/{self.id}/favorites/user/{self._client.username}",
            headers=self._headers,
        ).json()["userFavorite"]

    def unfavorite(self):
        self._client._ensure_logged_in()

        return requests.delete(
            f"https://api.scratch.mit.edu/proxy/projects/{self.id}/favorites/user/{self._client.username}",
            headers=self._headers,
        ).json()["userFavorite"]

    def get_scripts(self):
        return requests.get(f"https://projects.scratch.mit.edu/{self.id}/").json()

    def save(self, project):
        self._client._ensure_logged_in()

        if self.author.username != self._client.username:
            raise UnauthorizedException("You are not allowed to do that")

        requests.put(
            f"https://projects.scratch.mit.edu/{self.id}",
            headers=self._json_headers,
            data=project,
        )

    def get_remixes(self, all=False, limit=20, offset=0):
        return get_data_list(
            all,
            limit,
            offset,
            f"https://api.scratch.mit.edu/projects/{self.id}/remixes",
            lambda project: Project(project, self._client),
        )

    def get_remixtree(self):
        response = requests.get(
            f"https://scratch.mit.edu/projects/{self.id}/remixtree/bare"
        )

        if response.text == "no data" or response.status_code == 404:
            return []

        tree = []
        for key, value in response.json().items():
            if key == "root_id":
                continue

            tree.append(
                RemixtreeProject(
                    {
                        **value,
                        "id": key,
                    }
                )
            )

        return tree

    def get_studios(self, all=False, limit=20, offset=0):
        return get_data_list(
            all,
            limit,
            offset,
            f"https://api.scratch.mit.edu/users/{self.author.username}/projects/{self.id}/studios",
            lambda studio: Studio(studio, self._client),
        )

    def post_comment(self, content, parent_id="", commentee_id=""):
        self._client._ensure_logged_in()

        if not self.comments_allowed:
            raise UnauthorizedException("Comments are closed on this project")

        data = {
            "commentee_id": commentee_id,
            "content": content,
            "parent_id": parent_id,
        }
        response = requests.post(
            f"https://api.scratch.mit.edu/proxy/comments/project/{self.id}/",
            headers=self._json_headers,
            data=json.dumps(data),
        ).json()

        if "rejected" in response:
            raise RejectedException("Your comment did not post")

        return ProjectComment(self, response, self._client)

    def get_comments(self, all=False, limit=20, offset=0):
        return get_data_list(
            all,
            limit,
            offset,
            f"https://api.scratch.mit.edu/users/{self.author.username}/projects/{self.id}/comments",
            lambda comment: ProjectComment(self, comment, self._client),
        )

    def get_cloud_logs(self, all=False, limit=20, offset=0):
        return get_data_list(
            all,
            limit,
            offset,
            "https://clouddata.scratch.mit.edu/logs",
            lambda log: log,
            params=f"&projectid={self.id}",
            headers=self._headers,
        )

    def get_visibility(self):
        self._ensure_logged_in()

        return requests.get(
            f"https//api.scratch.mit.edu/users/{self._client.username}/projects/{self.id}/visibility",
            headers=self._headers,
        ).json()

    def toggle_commenting(self):
        self._client._ensure_logged_in()

        if self.author.username != self._client.username:
            raise UnauthorizedException("You are not allowed to do that")

        data = {"comments_allowed": not self.comments_allowed}
        self.comments_allowed = not self.comments_allowed
        return Project(
            requests.put(
                f"https://api.scratch.mit.edu/projects/{self.id}/",
                data=json.dumps(data),
                headers=self._json_headers,
            ).json(),
            self._client,
        )

    def turn_on_commenting(self):
        self._client._ensure_logged_in()

        if self.author.username != self._client.username:
            raise UnauthorizedException("You are not allowed to do that")

        data = {"comments_allowed": True}
        self.comments_allowed = True
        return Project(
            requests.put(
                f"https://api.scratch.mit.edu/projects/{self.id}/",
                data=json.dumps(data),
                headers=self._json_headers,
            ).json(),
            self._client,
        )

    def turn_off_commenting(self):
        self._client._ensure_logged_in()

        if self.author.username != self._client.username:
            raise UnauthorizedException("You are not allowed to do that")

        data = {"comments_allowed": False}
        self.comments_allowed = False
        return Project(
            requests.put(
                f"https://api.scratch.mit.edu/projects/{self.id}/",
                data=json.dumps(data),
                headers=self._json_headers,
            ).json(),
            self._client,
        )

    def report(self, category, reason, image=None):
        self._client._ensure_logged_in()

        if not image:
            image = self.thumbnail_URL
        data = {"notes": reason, "report_category": category, "thumbnail": image}

        requests.post(
            f"https://api.scratch.mit.edu/proxy/comments/project/{self.id}/",
            data=json.dumps(data),
            headers=self._json_headers,
        )

    def unshare(self):
        self._client._ensure_logged_in()

        if self.author.username != self._client.username:
            raise UnauthorizedException("You are not allowed to do that")

        requests.put(
            f"https://api.scratch.mit.edu/proxy/projects/{self.id}/unshare/",
            headers=self._json_headers,
        )

        self.public = False

    def share(self):
        self._client._ensure_logged_in()

        if self.author.username != self._client.username:
            raise UnauthorizedException("You are not allowed to do that")

        requests.put(
            f"https://api.scratch.mit.edu/proxy/projects/{self.id}/share/",
            headers=self._json_headers,
        )

        self.public = True

    def delete(self):
        self._client._ensure_logged_in()

        if self.author.username != self._client.username:
            raise UnauthorizedException("You are not allowed to do that")

        data = {"visibility": "trshbyusr"}

        requests.put(
            f"https://scratch.mit.edu/site-api/projects/all/{self.id}/",
            data=json.dumps(data),
            headers=self._json_headers,
        )

    def restore_deleted(self):
        self._client._ensure_logged_in()

        if self.author.username != self._client.username:
            raise UnauthorizedException("You are not allowed to do that")

        data = {"visibility": "visible"}

        requests.put(
            f"https://scratch.mit.edu/site-api/projects/all/{self.id}/",
            data=json.dumps(data),
            headers=self._json_headers,
        )

    def view(self):
        requests.post(
            f"https://api.scratch.mit.edu/users/{self.author.username}/projects/{self.id}/views/",
            headers=self._headers,
        )

    def set_thumbnail(self, file_or_data):
        self._client._ensure_logged_in

        if self.author.username != self._client.username:
            raise UnauthorizedException("You are not allowed to do that")

        data = (
            file_or_data
            if isinstance(file_or_data, bytes)
            else open(file_or_data, "rb").read()
        )
        requests.post(
            f"https://scratch.mit.edu/internalapi/project/thumbnail/{self.id}/set",
            data=data,
            headers=self._headers,
        )

    def set_title(self, title):
        self._client._ensure_logged_in()

        if self.author.username != self._client.username:
            raise UnauthorizedException("You are not allowed to do that")

        data = {"title": title}
        requests.put(
            f"https://api.scratch.mit.edu/projects/{self.id}/",
            data=json.dumps(data),
            headers=self._json_headers,
        )

        self.title = title

    def set_instructions(self, instructions):
        self._client._ensure_logged_in()

        if self.author.username != self._client.username:
            raise UnauthorizedException("You are not allowed to do that")

        data = {"instructions": instructions}
        requests.put(
            f"https://api.scratch.mit.edu/projects/{self.id}/",
            data=json.dumps(data),
            headers=self._json_headers,
        )

        self.instructions = instructions

    def set_description(self, description):
        self._client._ensure_logged_in()

        if self.author.username != self._client.username:
            raise UnauthorizedException("You are not allowed to do that")

        data = {"description": description}
        requests.put(
            f"https://api.scratch.mit.edu/projects/{self.id}/",
            data=json.dumps(data),
            headers=self._json_headers,
        )

        self.description = description
