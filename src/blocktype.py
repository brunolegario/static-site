import re
from enum import Enum
from htmlnode import ParentNode
from textnode import TextNode, TextType
from inline_markdown import text_to_textnodes

class BlockType(Enum):
  PARAGRAPH = "paragraph"
  HEADING = "heading"
  CODE = "code"
  QUOTE = "quote"
  UNORDERED_LIST = "unordered_list"
  ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
  blocks = []
  lines = markdown.split("\n\n")

  for line in lines:
    line = line.strip()
    if line == "":
      continue
    blocks.append(line)
  
  return blocks

def block_to_blocktype(block):
  if block.startswith("- "):
    return BlockType.UNORDERED_LIST
  elif re.match(r"^\d+\. ", block):
    return BlockType.ORDERED_LIST
  elif block.startswith("```") and block.endswith("```"):
    return BlockType.CODE
  elif block.startswith("> "):
    return BlockType.QUOTE
  elif re.match(r"^#{1,6} ", block):
    return BlockType.HEADING
  else:
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
  blocks = markdown_to_blocks(markdown)
  html_nodes = []

  for block in blocks:
    block_type = block_to_blocktype(block)
    html_node = block_to_html_node(block, block_type)
    html_nodes.append(html_node)
  
  parent = ParentNode("div", children=html_nodes)
  return parent

def block_to_html_node(block, block_type):
  if block_type == BlockType.PARAGRAPH:
    text_nodes = text_to_children(block)
    return ParentNode("p", children=text_nodes)

  elif block_type == BlockType.HEADING:
    level = len(re.match(r"^(#+)", block).group(1))
    heading_text = block[level + 1 :].strip()
    text_nodes = text_to_children(heading_text)
    return ParentNode(f"h{level}", children=text_nodes)

  elif block_type == BlockType.CODE:
    code_text = block[3:-3].strip()
    text_node = TextNode(code_text, TextType.PLAIN).to_html()
    return ParentNode("pre", children=[ParentNode("code", children=[text_node])])

  elif block_type == BlockType.QUOTE:
    quote_text = block[2:].strip()
    text_nodes = text_to_children(quote_text)
    return ParentNode("blockquote", children=text_nodes)

  elif block_type == BlockType.UNORDERED_LIST:
    items = [item[2:].strip() for item in block.split("\n") if item.startswith("- ")]
    li_nodes = []
    for item in items:
      text_nodes = text_to_children(item)
      li_nodes.append(ParentNode("li", children=text_nodes))
    return ParentNode("ul", children=li_nodes)

  elif block_type == BlockType.ORDERED_LIST:
    items = [re.sub(r"^\d+\. ", "", item).strip() for item in block.split("\n") if re.match(r"^\d+\. ", item)]
    li_nodes = []
    for item in items:
      text_nodes = text_to_children(item)
      li_nodes.append(ParentNode("li", children=text_nodes))
    return ParentNode("ol", children=li_nodes)

  else:
    raise ValueError(f"Unsupported block type: {block_type}")


def text_to_children(text):
  text_nodes = text_to_textnodes(text)
  leaf_nodes = [node.to_html() for node in text_nodes]
  return leaf_nodes