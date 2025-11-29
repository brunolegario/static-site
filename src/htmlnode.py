class HTMLNode:
  def __init__(self, tag=None, value=None, children=None, props=None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  def to_html(self):
    raise NotImplementedError("Subclasses should implement this method")

  def props_to_html(self):
    if not self.props:
      return ""
    props_str = ""
    for key, value in self.props.items():
      props_str += f' {key}="{value}"'
    return props_str

  def __eq__(self, other):
    return (
      isinstance(other, HTMLNode) and
      self.tag == other.tag and
      self.value == other.value and
      self.children == other.children and
      self.props == other.props
    )

  def __repr__(self):
    return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

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