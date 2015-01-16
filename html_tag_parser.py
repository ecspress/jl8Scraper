"""Parses and finds all link and image tags in an html document"""
from html.parser import HTMLParser


class Tag:
    """Stores data regarding link and image tags in HTML."""

    def __init__(self, tag):
        self.data = None
        self.tag = tag
        self.attributes = dict()

    def add_data(self, data):
        """Stores the text of a tag.

        Input:
            text between start and end of a tag.

        Output:
            None

        Raises:
            None
        """
        self.data = data

    def add_attribute(self, attribute_name, attribute_value):
        """Stores the attributes of a tag in a dictionary.

        Input:
            AttributeName, AttributeValue

        Output:
            None

        Raises:
            None
        """
        self.attributes[attribute_name] = attribute_value


class HTMLTagParser(HTMLParser):
    """Parses image and link tags in HTML"""

    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []
        self.images = []
        self.current_tags = []

    def parse(self, data):
        """Initializes and resets the parser.

        Input:
            data to be parsed

        Output:
            None

        Raises:
            None
        """
        self.links = []
        self.images = []
        self.current_tags = []
        self.reset()
        self.feed(data)

    def handle_starttag(self, tag, attrs):
        """Handles the start of a tag.

        Input:
            tagName, attributes of the tag as tuples(key, value)

        Output:
            None

        Raises:
            None
        """
        if tag == "a":
            curr_tag = Tag(tag)
            for attribute in attrs:
                curr_tag.add_attribute(attribute[0], attribute[1])
            self.current_tags.append(curr_tag)
        elif tag == "img":
            curr_tag = Tag(tag)
            for attribute in attrs:
                curr_tag.add_attribute(attribute[0], attribute[1])
            self.images.append(curr_tag)


    def handle_endtag(self, tag):
        """Handles the end of a tag.

        Input:
            tagName

        Output:
            None

        Raises:
            None
        """
        if tag == "a":
            self.links.append(self.current_tags.pop())

    def handle_data(self, data):
        """Handles the text of a tag.

        Input:
            text of tag

        Output:
            None

        Raises:
            None
        """
        if len(self.current_tags) > 0:
            self.current_tags[-1].add_data(data)

def test_main():
    """Tests the current module"""
    parser = HTMLTagParser()
    parser.parse('<img>some text</img><a href="www"><t>,</t>linkkkk</a>')
    for link in parser.links:
        print(link.attributes, link.data)
    for image in parser.images:
        print(image.attributes, image.data)


if __name__ == "__main__":
    test_main()
