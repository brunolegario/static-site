from textnode import TextNode, TextType
from inline_markdown import text_to_textnodes
from blocktype import markdown_to_html_node

def main():
  # node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
  # print(node)

  md = """
This is **bolded** paragraph
text in a p
tag here

> This is another paragraph with _italic_ text and `code` here

1. First item
2. Second item

```
def example():
    print("Hello, World!")
```

- Unordered item one
- Unordered item two
"""

  html_node = markdown_to_html_node(md)
  print(html_node.to_html())

main()