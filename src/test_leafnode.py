import unittest
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
  def test_leaf_to_html_p(self):
    node = LeafNode("p", "Hello, world!")
    self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

  def test_leaf_to_html_span_with_props(self):
    node = LeafNode("span", "Important", props={"class": "highlight"})
    self.assertEqual(node.to_html(), '<span class="highlight">Important</span>')

  def test_leaf_to_html_no_tag(self):
    node = LeafNode(None, "Just some text")
    self.assertEqual(node.to_html(), "Just some text")

  def test_leaf_to_html_no_value_raises(self):
    node = LeafNode("p", None)
    with self.assertRaises(ValueError):
      node.to_html()

if __name__ == '__main__':
  unittest.main()