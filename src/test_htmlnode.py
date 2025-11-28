import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
  def test_eq(self):
    node1 = HTMLNode("div", "This is a div")
    node2 = HTMLNode("div", "This is a div")
    self.assertEqual(node1, node2)

  def test_not_eq_different_html(self):
    node1 = HTMLNode("div", "This is a div")
    node2 = HTMLNode("span", "This is a span")
    self.assertNotEqual(node1, node2)

  def test_not_eq_different_props(self):
    node1 = HTMLNode("div", "This is a div", props={"class": "container"})
    node2 = HTMLNode("div", "This is a div", props={"id": "main"})
    self.assertNotEqual(node1, node2)

  def test_props_to_html(self):
    node = HTMLNode("div", "This is a div", props={"class": "container", "id": "main"})
    expected_html = ' class="container" id="main"'
    self.assertEqual(node.props_to_html(), expected_html)

if __name__ == '__main__':
  unittest.main()