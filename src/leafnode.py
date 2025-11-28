from htmlnode import HTMLNode

class LeafNode(HTMLNode):
  def __init__(self, tag, value, props=None):
    super().__init__(tag, value, None, props)

  def to_html(self):
    if self.value is None:
      raise ValueError("LeafNode must have a value to convert to HTML")

    if self.tag is None:
      return str(self.value)

    props_str = self.props_to_html()
    return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
    