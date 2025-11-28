from htmlnode import HTMLNode

class ParentNode(HTMLNode):
  def __init__(self, tag, children, props=None):
    super().__init__(tag, None, children, props)

  def to_html(self):
    if self.tag is None:
      raise ValueError("ParentNode must have a tag to convert to HTML")

    if self.children is None or len(self.children) == 0:
      raise ValueError("ParentNode must have children to convert to HTML")
    
    props_str = self.props_to_html()
    children_html = "".join(child.to_html() for child in self.children)

    return f"<{self.tag}{props_str}>{children_html}</{self.tag}>"