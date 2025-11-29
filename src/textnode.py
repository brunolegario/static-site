from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    UNDERLINE = "underline"
    STRIKETHROUGH = "strikethrough"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
  def __init__(self, text, text_type, url = None):
    self.text = text
    self.text_type = text_type
    self.url = url

  def __eq__(self, other):
    return (
      isinstance(other, TextNode) and
      self.text == other.text and
      self.text_type == other.text_type and
      self.url == other.url
    )

  def __repr__(self):
    return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

  def to_html(self):
    if self.text_type == TextType.PLAIN:
      return LeafNode(None, self.text)
    elif self.text_type == TextType.BOLD:
      return LeafNode("b", self.text)
    elif self.text_type == TextType.ITALIC:
      return LeafNode("i", self.text)
    elif self.text_type == TextType.UNDERLINE:
      return LeafNode("u", self.text)
    elif self.text_type == TextType.STRIKETHROUGH:
      return LeafNode("s", self.text)
    elif self.text_type == TextType.CODE:
      return LeafNode("code", self.text)
    elif self.text_type == TextType.LINK:
      if self.url is None:
        raise ValueError("URL must be provided for link text type")
      return LeafNode("a", self.text, props={"href": self.url})
    elif self.text_type == TextType.IMAGE:
      if self.url is None:
        raise ValueError("URL must be provided for image text type")
      return LeafNode("img", "", props={"src": self.url, "alt": self.text})
    else:
      raise Exception("Error: Unsupported text type")