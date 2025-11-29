import unittest
from textnode import TextNode, TextType
from inline_markdown import (
  split_nodes_delimiter, 
  split_nodes_image, 
  split_nodes_link, 
  extract_markdown_images, 
  extract_markdown_links, 
  text_to_textnodes
)

class TestSplitters(unittest.TestCase):
  def test_split_nodes_delimiter(self):
    old_nodes = [TextNode("This is text with a `code block` word", TextType.PLAIN)]
    delimiter = "`"
    text_type = TextType.CODE

    expected_new_nodes = [
      TextNode("This is text with a ", TextType.PLAIN),
      TextNode("code block", TextType.CODE),
      TextNode(" word", TextType.PLAIN)
    ]

    new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
    self.assertEqual(new_nodes, expected_new_nodes)

  def test_split_nodes_delimiter_invalid_syntax(self):
    old_nodes = [TextNode("This is text with no delimiters", TextType.PLAIN)]
    delimiter = "`"
    text_type = TextType.CODE
  
    expected_new_nodes = [
      TextNode("This is text with no delimiters", TextType.PLAIN)
    ]

    new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
    self.assertEqual(new_nodes, expected_new_nodes)

  def test_split_nodes_delimiter_odd_delimiters(self):
    old_nodes = [TextNode("This is text with a **bold block** and another **bold block**", TextType.PLAIN)]
    delimiter = "**"
    text_type = TextType.BOLD

    expected_new_nodes = [
      TextNode("This is text with a ", TextType.PLAIN),
      TextNode("bold block", TextType.BOLD),
      TextNode(" and another ", TextType.PLAIN),
      TextNode("bold block", TextType.BOLD)
    ]

    new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
    self.assertEqual(new_nodes, expected_new_nodes)

  def test_split_images(self):
    node = TextNode(
      "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
      TextType.PLAIN,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
      [
        TextNode("This is text with an ", TextType.PLAIN),
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and another ", TextType.PLAIN),
        TextNode(
          "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
        ),
      ],
      new_nodes,
    )

  def test_split_nodes_link(self):
    old_nodes = [TextNode("Here is a link [link text](http://example.com) in the text.", TextType.PLAIN)]

    expected_new_nodes = [
      TextNode("Here is a link ", TextType.PLAIN),
      TextNode("link text", TextType.LINK, "http://example.com"),
      TextNode(" in the text.", TextType.PLAIN)
    ]

    new_nodes = split_nodes_link(old_nodes)
    self.assertEqual(new_nodes, expected_new_nodes)

  def test_text_to_textnodes(self):
    node = TextNode("This is **bold** text with an ![image](http://image.url) and a [link](http://link.url) and a `code block`.", TextType.PLAIN)
    
    expected_new_nodes = [
      TextNode("This is ", TextType.PLAIN),
      TextNode("bold", TextType.BOLD),
      TextNode(" text with an ", TextType.PLAIN),
      TextNode("image", TextType.IMAGE, "http://image.url"),
      TextNode(" and a ", TextType.PLAIN),
      TextNode("link", TextType.LINK, "http://link.url"),
      TextNode(" and a ", TextType.PLAIN),
      TextNode("code block", TextType.CODE),
      TextNode(".", TextType.PLAIN)
    ]

    new_nodes = text_to_textnodes(node)
    self.assertEqual(new_nodes, expected_new_nodes)

if __name__ == '__main__':
  unittest.main()
