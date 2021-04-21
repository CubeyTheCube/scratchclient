import requests
import json


class UserProfile:
    def __init__(self, data, user):
        self.user = user
        self.username = user.username
        self.id = data["id"]
        self.avatar_URL = data["images"]["90x90"]
        self.bio = data["bio"]
        self.status = data["status"]
        self.country = data["country"]

    def set_bio(self, content):
        data = {"bio": content}
        return requests.put(
            "https://scratch.mit.edu/site-api/users/all/" + self.username + "/",
            data=data,
            headers=self.user._headers,
        )

    def set_status(self, content):
        data = {"status": content}
        return requests.put(
            "https://scratch.mit.edu/site-api/users/all/" + self.username + "/",
            data=data,
            headers=self.user._headers,
        )

    def set_featured_project(self, label, project):
        label = (
            {
                "featured_project": "",
                "featured_tutorial": 0,
                "work_in_progress": 1,
                "remix_this": 2,
                "my_favorite_things": 3,
                "why_i_scratch": 4,
            }
        )[label]
        project_id = project.id if isinstance(project, Project) else project
        data = {"featured_project": project_id, "featured_project_label": label}
        requests.put(
            "https://scratch.mit.edu/site-api/users/all/" + self.username + "/",
            data=json.dumps(data),
            headers=self._headers,
        )
