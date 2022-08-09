import requests
import xml.etree.ElementTree

from .ScratchExceptions import *

ns = {"atom": "http://www.w3.org/2005/Atom"}


class ForumPost:
    def __init__(self, data):
        self.title = data["title"]
        self.link = data["link"]
        self.published = data["published"]

        self.author = data["author"]
        self.id = data["id"]
        self.content = data["summary"]


class ForumSession:
    def __init__(self, client):
        self._client = client
        self._headers = {
            "x-csrftoken": self._client.csrf_token,
            "X-Token": self._client.token,
            "x-requested-with": "XMLHttpRequest",
            "Cookie": f"scratchcsrftoken={self._client.csrf_token};scratchlanguage=en;scratchsessionsid={self._client.session_id};",
        }

    def create_topic(self, category_id, title, body):
        self._client._ensure_logged_in()

        headers = {
            **self._headers,
            "referer": f"https://scratch.mit.edu/discuss/{category_id}/topic/add",
        }

        data = {
            "csrfmiddlewaretoken": self._client.csrf_token,
            "name": title,
            "body": body,
            "subscribe": "on",
            "AddPostForm": "",
        }

        requests.post(
            f"https://scratch.mit.edu/discuss/{category_id}/topic/add",
            headers=headers,
            files=data,
        )

    def post(self, topic_id, content):
        self._client._ensure_logged_in()

        headers = {
            **self._headers,
            "referer": f"https://scratch.mit.edu/discuss/topic/{topic_id}/",
        }

        response = requests.post(
            f"https://scratch.mit.edu/discuss/topic/{topic_id}/?",
            headers=headers,
            files={
                "csrfmiddlewaretoken": self._client.csrf_token,
                "body": content,
                "AddPostForm": "",
            },
        )

        if response.status_code == 403:
            raise UnauthorizedException("This topic is closed")

    def edit_post(self, post_id, content):
        self._client._ensure_logged_in()

        headers = {
            **self._headers,
            "referer": f"https://scratch.mit.edu/discuss/post/{post_id}/edit",
        }

        data = {
            "csrfmiddlewaretoken": self._client.csrf_token,
            "body": content,
        }

        response = requests.post(
            f"https://scratch.mit.edu/discuss/post/{post_id}/edit",
            headers=headers,
            data=data,
        )

        if response.status_code == 403:
            raise UnauthorizedException("This post is not yours")

    def report_post(self, post_id, reason):
        self._client._ensure_logged_in()

        headers = {
            **self._headers,
            "referer": f"https://scratch.mit.edu/discuss/misc/?action=report&post_id={post_id}",
        }

        data = {
            "csrfmiddlewaretoken": self._client.csrf_token,
            "post": post_id,
            "reason": reason,
            "submit": "",
        }

        requests.post(
            f"https://scratch.mit.edu/discuss/misc/?action=report&post_id={post_id}",
            headers=headers,
            data=data,
        )

    def get_post_source(self, post_id):
        return requests.get(
            f"https://scratch.mit.edu/discuss/post/{post_id}/source/",
        ).text

    def follow_topic(self, topic_id):
        self._client._ensure_logged_in()

        headers = {
            **self._headers,
            "referer": f"https://scratch.mit.edu/discuss/topic/{topic_id}/",
        }

        requests.post(
            f"https://scratch.mit.edu/discuss/subscription/topic/{topic_id}/add/",
            headers=headers,
        )

    def unfollow_topic(self, topic_id):
        self._client._ensure_logged_in()

        headers = {
            **self._headers,
            "referer": f"https://scratch.mit.edu/discuss/topic/{topic_id}/",
        }

        requests.post(
            f"https://scratch.mit.edu/discuss/subscription/topic/{topic_id}/delete/",
            headers=headers,
        )

    def change_signature(self, signature):
        self._client._ensure_logged_in()

        headers = {
            **self._headers,
            "referer": f"https://scratch.mit.edu/discuss/settings/{self._client.username}/",
        }

        data = {
            "csrfmiddlewaretoken": self._client.csrf_token,
            "signature": signature,
            "update": "",
        }

        requests.post(
            f"https://scratch.mit.edu/discuss/settings/{self._client.username}/",
            headers=headers,
            data=data,
        )

    def get_latest_topic_posts(self, topic_id):
        rss_feed = requests.get(
            f"https://scratch.mit.edu/discuss/feeds/topic/{topic_id}/",
        ).text
        root = xml.etree.ElementTree.fromstring(rss_feed)

        return [
            ForumPost(
                {
                    "title": post.find("atom:title", ns).text,
                    "link": post.find("atom:link", ns).attrib["href"],
                    "published": post.find("atom:published", ns).text,
                    "author": post.find("atom:author", ns).find("atom:name", ns).text,
                    "id": int(post.find("atom:id", ns).text),
                    "summary": post.find("atom:summary", ns).text,
                }
            )
            for post in root.findall("atom:entry", ns)
        ]

    def get_latest_category_posts(self, category_id):
        rss_feed = requests.get(
            f"https://scratch.mit.edu/discuss/feeds/forum/{category_id}/",
        ).text
        root = xml.etree.ElementTree.fromstring(rss_feed)

        return [
            ForumPost(
                {
                    "title": post.find("atom:title", ns).text,
                    "link": post.find("atom:link", ns).attrib["href"],
                    "published": post.find("atom:published", ns).text,
                    "author": post.find("atom:author", ns).find("atom:name", ns).text,
                    "id": int(post.find("atom:id", ns).text),
                    "summary": post.find("atom:summary", ns).text,
                }
            )
            for post in root.findall("atom:entry", ns)
        ]
