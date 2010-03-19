
class TagCollection:
    def __init__(self):
        self.tags = []
        self.tag_chars = "abcdefghijklmopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#-:_ +"

    def clear(self):
        self.tags = []

    def export_to_datastore(self):
        s = ""
        for tag in self.tags:
            if tag != self.tags[0]:
                s += ","
            s += tag
        return s

    def filter_tag(self, tag):
        return "" + "".join([c for c in tag if c in self.tag_chars])

    def get_tags(self):
        return self.tags

    def import_raw_tags(self, tags):
        self.raw_tags = tags

    def import_string(self, str):
        raw_tags = str.split(",")
        tags = []
        for raw_tag in raw_tags:
            tag = self.filter_tag(raw_tag)
            if tag != "":
                tags.append(tag)
        self.tags.extend(tags)
        return tags
