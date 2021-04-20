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
        requests.delete(
            "https://api.scratch.mit.edu/proxy/comments/project/"
            + str(self.project.id)
            + "/comment/"
            + str(self.id),
            headers=self.project._headers,
        )

    def report(self):
        requests.post(
            "https://api.scratch.mit.edu/proxy/comments/project/"
            + str(self.project.id)
            + "/comment/"
            + str(self.id)
            + "/report",
            headers=self.project._headers,
        )

    def reply(self, content):
        self.project.post_comment(content, self.id, self.author_id)
