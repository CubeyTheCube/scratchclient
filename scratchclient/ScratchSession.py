import requests
import re
import json
import hashlib
import pathlib

from .ScratchExceptions import *
from .User import User
from .Project import Project
from .Studio import Studio
from .News import News
from .Message import Message
from .CloudConnection import CloudConnection, AsyncCloudConnection
from .Forums import ForumSession
from .Scraping import ScrapingSession
from .Backpack import BackpackItem
from .Incomplete import *
from .Comment import ProjectComment
from .Activity import Activity
from .util import get_data_list


class ScratchSession:
    def __init__(self, username=None, password=None, session_id=None, token=None):
        self.logged_in = False
        self.username = username
        self.session_id = session_id
        self.csrf_token = None
        self.token = token
        if password:
            self.login(password)

        if self.session_id or self.token:
            self.get_csrf_token()
            self.logged_in = True

        self.forums = ForumSession(self)
        self.scraping = ScrapingSession(self)

        self._headers = {
            "x-csrftoken": self.csrf_token,
            "X-Token": self.token,
            "x-requested-with": "XMLHttpRequest",
            "Cookie": f"scratchcsrftoken={self.csrf_token};scratchlanguage=en;scratchsessionsid={self.session_id};",
            "referer": f"https://scratch.mit.edu/",
        }

        self.user = self.get_user(self.username) if self.logged_in else None

    def login(self, password):
        # logs in to Scratch
        headers = {
            "x-csrftoken": "a",
            "x-requested-with": "XMLHttpRequest",
            "Cookie": "scratchcsrftoken=a;scratchlanguage=en;",
            "referer": "https://scratch.mit.edu",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
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

        self.get_csrf_token()

    def get_csrf_token(self):
        headers = {
            "x-requested-with": "XMLHttpRequest",
            "Cookie": "scratchlanguage=en;permissions=%7B%7D;",
            "referer": "https://scratch.mit.edu",
        }

        request = requests.get("https://scratch.mit.edu/csrf_token/", headers=headers)

        self.csrf_token = re.search(
            "scratchcsrftoken=(.*?);", request.headers["Set-Cookie"]
        ).group(1)

    def logout(self):
        self._client._ensure_logged_in()

        requests.post(
            "https://scratch.mit.edu/accounts/logout/",
            data={"csrfmiddlewaretoken": self.csrf_token},
        )

    def check_password(self, password):
        self._client._ensure_logged_in()

        data = {
            "csrfmiddlewaretoken": self.csrf_token,
            "password": password,
        }

        response = requests.post(
            "https://scratch.mit.edu/accounts/check_password",
            data=json.dumps(data),
            headers=self._headers,
        ).json()

        return response["success"]

    def get_user(self, user):
        username = user.username if isinstance(user, (IncompleteUser, User)) else user
        return User(
            requests.get(
                f"https://api.scratch.mit.edu/users/{username}/",
                headers=self._headers,
            ).json(),
            self,
        )

    def get_project(self, project):
        project_id = (
            project.id
            if isinstance(project, (IncompleteProject, RemixtreeProject, Project))
            else project
        )
        return Project(
            requests.get(
                f"https://api.scratch.mit.edu/projects/{project_id}/",
                headers=self._headers,
            ).json(),
            self,
        )

    def get_studio(self, studio):
        studio_id = (
            studio.id if isinstance(studio, (IncompleteStudio, Studio)) else studio
        )
        return Studio(
            requests.get(
                f"https://api.scratch.mit.edu/studios/{studio}/",
                headers=self._headers,
            ).json(),
            self,
        )

    def get_news(self, all=False, limit=20, offset=0):
        return get_data_list(
            all,
            limit,
            offset,
            f"https://api.scratch.mit.edu/news/",
            News,
        )

    def get_messages(self, all=False, limit=20, offset=0, filter=""):
        return get_data_list(
            all,
            limit,
            offset,
            f"https://api.scratch.mit.edu/users/{self.username}/messages",
            Message,
            params=f"&filter={filter}",
            headers=self._headers,
        )

    def create_cloud_connection(self, project_id, is_async=False, cloud_host="clouddata.scratch.mit.edu", headers={}):
        return (
            AsyncCloudConnection(project_id, self, cloud_host, headers)
            if is_async
            else CloudConnection(project_id, self, cloud_host, headers)
        )

    def explore_projects(self, mode="trending", query="*", language="en"):
        return [
            Project(project, self)
            for project in requests.get(
                f"https://api.scratch.mit.edu/explore/projects/?mode={mode}&q={query}&language={language}"
            ).json()
        ]

    def explore_studios(self, mode="trending", query="*"):
        return [
            Studio(studio, self)
            for studio in requests.get(
                f"https://api.scratch.mit.edu/explore/studios/?mode={mode}&q={query}"
            ).json()
        ]

    def search_projects(self, mode="popular", query="*", language="en"):
        return [
            Project(project, self)
            for project in requests.get(
                f"https://api.scratch.mit.edu/search/projects/?mode={mode}&q={query}&language={language}"
            ).json()
        ]

    def search_studios(self, mode="popular", query="*"):
        return [
            Studio(studio, self)
            for studio in requests.get(
                f"https://api.scratch.mit.edu/search/studios/?mode={mode}&q={query}"
            ).json()
        ]

    def get_front_page(self):
        response = requests.get("https://api.scratch.mit.edu/proxy/featured").json()
        return {
            "featured_projects": [
                IncompleteProject(project)
                for project in response["community_featured_projects"]
            ],
            "featured_studios": [
                IncompleteStudio(studio)
                for studio in response["community_featured_studios"]
            ],
            "top_loved": [
                IncompleteProject(project)
                for project in response["community_most_loved_projects"]
            ],
            "top_remixed": [
                IncompleteProject(project)
                for project in response["community_most_remixed_projects"]
            ],
            "newest": [
                IncompleteProject(project)
                for project in response["community_newest_projects"]
            ],
            "curated": [
                IncompleteProject(project)
                for project in response["curator_top_projects"]
            ],
            "scratch_design_studio": [
                IncompleteProject(project)
                for project in response["scratch_design_studio"]
            ],
            "curator": response["curator_top_projects"][0]["curator_name"],
            "current_sds": IncompleteStudio(
                {
                    "id": response["scratch_design_studio"][0]["gallery_id"],
                    "title": response["scratch_design_studio"][0]["gallery_title"],
                    "thumbnail_url": f"""https://cdn2.scratch.mit.edu/get_image/gallery/{
                      response["scratch_design_studio"][0]["gallery_id"]
                    }_480x360.png""",
                }
            ),
        }

    def get_activity(self, limit=5, offset=0):
        self._ensure_logged_in()

        return [
            Activity(activity)
            for activity in requests.get(
                f"https://api.scratch.mit.edu/users/{self.username}/following/users/activity?limit={limit}&offset={offset}",
                headers=self._headers,
            ).json()
        ]

    def create_project(self, project):
        self._ensure_logged_in()

        response = requests.post(
            "https://projects.scratch.mit.edu/",
            headers={
                **self._headers,
                "accept": "application/json",
                "Content-Type": "application/json",
            },
            data=json.dumps(project),
        ).json()

        return int(response["content-name"])

    def create_studio(self):
        self._ensure_logged_in()

        response = requests.post(
            "https://scratch.mit.edu/studios/create/",
            headers={
                **self._headers,
                "referer": "https://scratch.mit.edu/mystuff/",
            },
            data=None,
        ).json()

        if response[0]["success"] == False:
            if response[0]["errors"][0].startswith("Woah"):
                raise RejectedException("You are creating studios too quickly")
            else:
                raise UnauthorizedException(
                    "You need to be a Scratcher to create a studio"
                )

        return int(re.search("\d+", response["redirect"]).group())

    def empty_trash(self, password):
        self._ensure_logged_in()

        data = {
            "models": [],
            "csrfmiddlewaretoken": self.csrf_token,
            "password": password,
        }

        response = requests.put(
            "https://scratch.mit.edu/site-api/projects/trashed/empty/",
            headers=self._headers,
            data=json.dumps(data),
        )

    def get_own_projects(self, all=False, sort="", filter="all", page=1):
        self._ensure_logged_in()

        def mystuff_project_to_project(project):
            return Project(
                {
                    "id": project["pk"],
                    "title": project["fields"]["title"],
                    "visibility": project["fields"]["visibility"],
                    "public": project["fields"]["isPublished"],
                    "comments_allowed": True,
                    "is_published": project["fields"]["isPublished"],
                    "author": {
                        "id": self.user.id,
                        "username": self.user.username,
                        "scratchteam": self.user.scratchteam,
                        "history": {
                            "joined": self.user.joined_timestamp,
                        },
                        "profile": {
                            "id": self.user.profile.id,
                            "images": {
                                "90x90": self.user.profile.avatar_URL,
                            },
                        },
                    },
                    "image": project["fields"]["thumbnail_url"],
                    "history": {
                        "created": project["fields"]["datetime_created"],
                        "modified": project["fields"]["datetime_modified"],
                        "shared": project["fields"]["datetime_shared"],
                    },
                    "stats": {
                        "views": project["fields"]["view_count"],
                        "loves": project["fields"]["love_count"],
                        "favorites": project["fields"]["favorite_count"],
                        "remixes": project["fields"]["remixers_count"],
                    },
                },
                self,
            )

        if all:
            projects = []
            while True:
                response = requests.get(
                    f"https://scratch.mit.edu/site-api/projects/{filter}/?page={page}&ascsort=&descsort={sort}",
                    headers=self._headers,
                )

                if response.status_code == 404:
                    break

                projects += response.json()
                page += 1

            return [mystuff_project_to_project(project) for project in projects]

        return [
            mystuff_project_to_project(project)
            for project in requests.get(
                f"https://scratch.mit.edu/site-api/projects/{filter}/?page={page}&ascsort=&descsort={sort}",
                headers=self._headers,
            ).json()
        ]

    def get_own_studios(self, all=False, sort="", page=1):
        self._ensure_logged_in()

        def mystuff_studio_to_studio(studio):
            return Studio(
                {
                    "id": studio["pk"],
                    "title": studio["fields"]["title"],
                    "host": studio["fields"]["owner"]["pk"],
                    "image": studio["fields"]["thumbnail_url"],
                    "visibility": "visible",
                    "open_to_all": False,
                    "comments_allowed": True,
                    "history": {
                        "created": studio["fields"]["datetime_created"],
                        "modified": studio["fields"]["datetime_modified"],
                    },
                    "stats": {
                        "comments": studio["fields"]["commenters_count"],
                        "curators": studio["fields"]["curators_count"],
                        "projects": studio["fields"]["projecters_count"],
                    },
                },
                self,
            )

        if all:
            studios = []
            while True:
                response = requests.get(
                    f"https://scratch.mit.edu/site-api/galleries/all/?page={page}&ascsort=&descsort={sort}",
                    headers=self._headers,
                )

                if response.status_code == 404:
                    break

                studios += response.json()
                page += 1

            return [mystuff_studio_to_studio(studio) for studio in studios]

        return [
            mystuff_studio_to_studio(studio)
            for studio in requests.get(
                f"https://scratch.mit.edu/site-api/galleries/all/?page={page}&ascsort=&descsort={sort}",
                headers=self._headers,
            ).json()
        ]

    def upload_asset(self, asset, file_ext=None):
        self._ensure_logged_in()

        data = asset if isinstance(asset, bytes) else open(asset, "rb").read()

        if isinstance(asset, str):
            file_ext = pathlib.Path(asset).suffix

        requests.post(
            f"https://assets.scratch.mit.edu/{hashlib.md5(data).hexdigest()}.{file_ext}",
            headers=self._headers,
            data=data,
        )

    def change_country(self, country):
        self._ensure_logged_in()

        data = {
            "csrfmiddlewaretoken": self.csrf_token,
            "country": country,
        }

        requests.post(
            "https://scratch.mit.edu/accounts/settings/",
            data=data,
            headers=self._headers,
        )

    def change_password(self, old_password, new_password):
        self._ensure_logged_in()

        data = {
            "csrfmiddlewaretoken": self.csrf_token,
            "old_password": old_password,
            "new_password1": new_password,
            "new_password2": new_password,
        }

        requests.post(
            "https://scratch.mit.edu/accounts/password_change/",
            data=data,
            headers=self._headers,
        )

    def change_email(self, new_email, password):
        self._ensure_logged_in()

        data = {
            "csrfmiddlewaretoken": self.csrf_token,
            "email_address": new_email,
            "password": password,
        }

        requests.post(
            "https://scratch.mit.edu/accounts/email_change/",
            data=data,
            headers=self._headers,
        )

    def change_email_subscription(self, activites=False, teacher_tips=False):
        self._ensure_logged_in()

        data = {
            "csrfmiddlewaretoken": self.csrf_token,
        }

        if activities:
            data["activites"] = "on"
        if teacher_tips:
            data["teacher_tips"] = "on"

        requests.post(
            "https://scratch.mit.edu/accounts/settings/update_subscription/",
            data=data,
            headers=self._headers,
        )

    def get_backpack(self, all=False, limit=20, offset=0):
        self._ensure_logged_in()

        return get_data_list(
            all,
            limit,
            offset,
            f"https://backpack.scratch.mit.edu/{self.username}",
            lambda item: BackpackItem(item, self),
            headers=self._headers,
        )

    def add_to_backpack(self, item_type, body, mime_type, name, thumbnail):
        self._ensure_logged_in()

        data = {
            "type": item_type,
            "body": body,
            "mime_type": mime_type,
            "name": name,
            "thumbnail": thumbnail,
        }

        requests.post(
            f"https://backpack.scratch.mit.edu/{self.username}",
            headers=self._headers,
            data=json.dumps(data),
        )

        return BackpackItem(data, self)

    def get_statistics(self):
        overall = requests.get(
            "https://scratch.mit.edu/statistics/data/daily/",
        ).json()
        last_month = requests.get(
            "https://scratch.mit.edu/statistics/data/monthly-ga/",
        ).json()
        over_time = requests.get(
            "https://scratch.mit.edu/statistics/data/monthly/"
        ).json()
        del overall["_TS"]
        del last_month["_TS"]
        del over_time["_TS"]

        return {
            **over_time,
            "overall": overall,
            "last_month": last_month,
        }

    def is_valid_username(self, username):
        response = requests.get(
            f"https://scratch.mit.edu/accounts/check_username/{username}/",
        ).json()

        return response[0].msg == "valid username"

    def _ensure_logged_in(self):
        if not self.logged_in:
            raise UnauthorizedException("You need to be logged in to do this")
