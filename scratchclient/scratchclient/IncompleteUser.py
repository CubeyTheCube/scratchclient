class IncompleteUser:
    def __init__(self, data):
        self.username = data["username"]
        self.id = data["id"]
        self.scratchteam = data["scratchteam"]
        self.joinedTimestamp = data["history"]["joined"]
        self.avatar_URL = data["profile"]["images"]["90x90"]
