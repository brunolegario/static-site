import unittest
from blocktype import markdown_to_blocks, block_to_blocktype, BlockType

class TestBlocks(unittest.TestCase):
  def test_markdown_to_blocks(self):
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

    blocks = markdown_to_blocks(md)
    self.assertEqual(
      blocks,
      [
        "This is **bolded** paragraph",
        "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
        "- This is a list\n- with items",
      ],
    )

  def test_block_to_blocktype(self):
    self.assertEqual(block_to_blocktype("- Item 1"), BlockType.UNORDERED_LIST)
    self.assertEqual(block_to_blocktype("1. Item 1"), BlockType.ORDERED_LIST)
    self.assertEqual(block_to_blocktype("```code block```"), BlockType.CODE)
    self.assertEqual(block_to_blocktype("> This is a quote"), BlockType.QUOTE)
    self.assertEqual(block_to_blocktype("## This is a heading"), BlockType.HEADING)
    self.assertEqual(block_to_blocktype("This is a normal paragraph."), BlockType.PARAGRAPH)

if __name__ == '__main__':
  unittest.main()