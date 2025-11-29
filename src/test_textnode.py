import unittest
from textnode import TextNode, TextType
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
  def test_eq(self):
    node1 = TextNode("This is a text node", TextType.BOLD)
    node2 = TextNode("This is a text node", TextType.BOLD)
    self.assertEqual(node1, node2)

  def test_not_eq_different_text(self):
    node1 = TextNode("This is a text node", TextType.BOLD)
    node2 = TextNode("This is a different text node", TextType.BOLD)
    self.assertNotEqual(node1, node2)

  def test_not_eq_different_type(self):
    node1 = TextNode("This is a text node", TextType.BOLD)
    node2 = TextNode("This is a text node", TextType.ITALIC)
    self.assertNotEqual(node1, node2)

  def test_eq_without_url(self):
    node1 = TextNode("Click here", TextType.LINK, None)
    node2 = TextNode("Click here", TextType.LINK)
    self.assertEqual(node1, node2)

  def test_to_html_bold(self):
    node = TextNode("Bold text", TextType.BOLD)
    self.assertEqual(node.to_html(), LeafNode("b", "Bold text"))

  def test_to_html_link_with_url(self):
    node = TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev")
    self.assertEqual(node.to_html(), LeafNode("a", "Boot.dev", props={"href": "https://www.boot.dev"}))

  def test_to_html_link_without_url_raises(self):
    node = TextNode("Boot.dev", TextType.LINK)
    with self.assertRaises(ValueError):
      node.to_html()
  
  def test_to_html_image_with_url(self):
    node = TextNode("An image", TextType.IMAGE, "https://www.example.com/image.png")
    self.assertEqual(node.to_html(), LeafNode("img", None, props={"src": "https://www.example.com/image.png", "alt": "An image"}))

  def test_text_to_html(self):
    node = TextNode("This is a text node", TextType.PLAIN)
    html_node = node.to_html()
    self.assertEqual(html_node.tag, None)
    self.assertEqual(html_node.value, "This is a text node")

if __name__ == '__main__':
  unittest.main()