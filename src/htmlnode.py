class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("This parent class does not have an implementation to render in HTML")

    def props_to_html(self):
        string = ""
        if self.props != None:
            for key, value in self.props.items():
                string += f" {key}=\"{value}\""
        return string

    def __eq__ (self, other):
        for property_name, property_value in vars(self).items():
            if property_value != getattr(other, property_name):
                return False
        return True

    def __repr__(self):
        properties = ""
        for property_name, property_value in vars(self).items():
            properties += f"{property_name}={property_value} "
        return f"{self.__class__.__name__}({properties})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str = None, value: str = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.props = props

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value!")
        if self.tag == None:
            html = f"{self.value}"
        else:
            html = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return html

class ParentNode(HTMLNode):
    def __init__(self, tag: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag == None or self.tag == "":
            raise ValueError("All parent nodes must have a valid tag!")

        if self.children == None or self.children == []:
            raise ValueError("All parent nodes must contain children!")

        innerhtml = ""
        for i in self.children:
            innerhtml += i.to_html()

        html = f"<{self.tag}{self.props_to_html()}>{innerhtml}</{self.tag}>"
        return html

