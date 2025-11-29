import unittest
from blocktype import markdown_to_blocks, block_to_blocktype, BlockType, markdown_to_html_node

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

  def test_markdown_to_html_node(self):
    md = """
This is **bolded** paragraph

- This is a list
- with items

1. First item
2. Second item

```
def example():
print("Hello, World!")
```
"""

    html_node = markdown_to_html_node(md)
    html_output = html_node.to_html()
    expected_html = (
      '<div>'
      '<p>This is <b>bolded</b> paragraph</p>'
      '<ul>'
      '<li>This is a list</li>'
      '<li>with items</li>'
      '</ul>'
      '<ol>'
      '<li>First item</li>'
      '<li>Second item</li>'
      '</ol>'
      '<pre><code>def example():\nprint("Hello, World!")</code></pre>'
      '</div>'
    )
    self.assertEqual(html_output, expected_html)

  def test_headings(self):
    md = """
# this is an h1

this is paragraph text

## this is an h2
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
    )
  
  def test_blockquote(self):
    md = """
> This is a
> blockquote block

this is paragraph text

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
    )

if __name__ == '__main__':
  unittest.main()