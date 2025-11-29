import unittest
from htmlnode import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):
  def test_parent_with_children_to_html(self):
    child1 = LeafNode("p", "Child paragraph 1")
    child2 = LeafNode("p", "Child paragraph 2")
    parent = ParentNode("div", children=[child1, child2], props={"class": "container"})
    expected_html = '<div class="container"><p>Child paragraph 1</p><p>Child paragraph 2</p></div>'
    self.assertEqual(parent.to_html(), expected_html)

  def test_parent_no_children_to_html(self):
    parent = ParentNode("div", children=[], props={"id": "empty"})
    with self.assertRaises(ValueError):
      parent.to_html()

  def test_parent_no_tag_to_html(self):
    child = LeafNode("p", "A child paragraph")
    parent = ParentNode(None, children=[child])
    with self.assertRaises(ValueError):
      parent.to_html()
    
  def test_to_html_with_grandchildren(self):
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )

if __name__ == '__main__':
  unittest.main()