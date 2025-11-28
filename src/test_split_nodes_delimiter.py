import unittest
from textnode import TextNode, TextType
from main import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
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

if __name__ == '__main__':
  unittest.main()
