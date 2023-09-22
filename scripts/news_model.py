from json import JSONEncoder


class News:
    def __init__(self, title, image_url, story, timestamp, link, source):
        self.title = title
        self.image_url = image_url
        self.story = story
        self.timestamp = timestamp
        self.link = link
        self.source = source


class NewsEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
