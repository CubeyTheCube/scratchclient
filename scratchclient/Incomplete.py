class IncompleteUser:
    def __init__(self, data):
        # Scratch API sometimes doesn't even return the username
        self.username = data["username"] if "username" in data else None
        self.id = data["id"]
        self.scratchteam = data["scratchteam"]
        self.joined_timestamp = data["history"]["joined"]
        self.avatar_URL = data["profile"]["images"]["90x90"]


class IncompleteProject:
    def __init__(self, data):
        self.title = data.pop("title")

        self.author = data.pop("creator" if "creator" in data else "username")
        self.id = data.pop("id")
        self.thumbnail_URL = data.pop(
            "thumbnail_url" if "thumbnail_url" in data else "image"
        )

        self.__dict__.update(data)


class RemixtreeProject:
    def __init__(self, data):
        self.id = data["id"]
        self.author = data["username"]
        self.moderation_status = data["moderation_status"]
        self.title = data["title"]

        self.created_timestamp = data["datetime_created"]["$date"]
        self.last_modified_timestamp = data["mtime"]["$date"]
        self.shared_timestamp = (
            data["datetime_shared"]["$date"] if data["datetime_shared"] else None
        )

        self.love_count = data["love_count"]
        self.favorite_count = data["favorite_count"]

        self.visible = data["visibility"] == "visible"
        self.is_published = data["is_published"]

        self.parent_id = int(data["parent_id"]) if data["parent_id"] else None
        self.children = [int(child) for child in data["children"]]


class IncompleteStudio:
    def __init__(self, data):
        self.title = data["title"]

        self.id = data["id"]
        self.thumbnail_URL = data["thumbnail_url"]
