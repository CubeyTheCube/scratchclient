class Message:
    def __init__(self, data):
        data["created_timestamp"] = data.pop("datetime_created")
        data["actor"] = data.pop("actor_username")
        self.__dict__.update(data)
