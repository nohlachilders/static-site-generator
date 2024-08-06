class TextNode:
    def __init__(self, text: str, text_type: str, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__ (self, other):
        for property_name, property_value in vars(self).items():
            if property_value != getattr(other, property_name):
                return False
        return True

    def __repr__ (self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

