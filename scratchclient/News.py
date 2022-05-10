class News:
    def __init__(self, data):
        self.id = data["id"]
        self.timestamp = data["stamp"]
        self.title = data["headline"]
        self.description = data["copy"]
        self.image_URL = data["image"]
        self.src = data["url"]
