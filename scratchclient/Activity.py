class Activity:
    def __init__(self, data):
        data["type"] = data.pop("type")
        data["created_timestamp"] = data.pop("datetime_created")
        data["actor"] = data.pop("actor_username")
        self.__dict__.update(data)
