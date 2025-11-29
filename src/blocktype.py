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
    html_node = block_to_html_node(block)
    html_nodes.append(html_node)
  
  parent = ParentNode("div", children=html_nodes)
  return parent

def block_to_html_node(block):
  block_type = block_to_blocktype(block)

  if block_type == BlockType.PARAGRAPH:
    return paragraph_to_html_node(block)

  elif block_type == BlockType.HEADING:
    return heading_to_html_node(block)

  elif block_type == BlockType.CODE:
    return code_to_html_node(block)

  elif block_type == BlockType.QUOTE:
    return quote_to_html_node(block)

  elif block_type == BlockType.UNORDERED_LIST:
    return ulist_to_html_node(block)

  elif block_type == BlockType.ORDERED_LIST:
    return olist_to_html_node(block)
  
  else:
    raise ValueError(f"Unsupported block type: {block_type}")

def paragraph_to_html_node(block):
  lines = block.split("\n")
  paragraph = " ".join(lines)
  children = text_to_children(paragraph)
  return ParentNode("p", children)

def heading_to_html_node(block):
  level = 0
  for char in block:
    if char == "#":
      level += 1
    else:
      break
  if level + 1 >= len(block):
    raise ValueError(f"Invalid heading level: {level}")
  text = block[level + 1 :].strip()
  children = text_to_children(text)
  return ParentNode(f"h{level}", children)

def code_to_html_node(block):
  if not (block.startswith("```") and block.endswith("```")):
    raise ValueError("Invalid code block")
  code_text = block[3:-3].strip()
  text_node = TextNode(code_text, TextType.PLAIN).to_html()
  code_node = ParentNode("code", children=[text_node])
  return ParentNode("pre", children=[code_node])

def quote_to_html_node(block):
  lines = block.split("\n")
  new_lines = []
  for line in lines:
    if not line.startswith("> "):
      raise ValueError("Invalid quote block")
    new_lines.append(line[2:].strip())
  content = " ".join(new_lines)
  text_nodes = text_to_children(content)
  return ParentNode("blockquote", children=text_nodes)

def olist_to_html_node(block):
  items = block.split("\n")
  li_nodes = []
  for item in items:
    text = re.sub(r"^\d+\. ", "", item).strip()
    children = text_to_children(text)
    li_nodes.append(ParentNode("li", children))
  return ParentNode("ol", children=li_nodes)

def ulist_to_html_node(block):
  items = block.split("\n")
  li_nodes = []
  for item in items:
    text = item[2:].strip()
    children = text_to_children(text)
    li_nodes.append(ParentNode("li", children))
  return ParentNode("ul", children=li_nodes)

def text_to_children(text):
  text_nodes = text_to_textnodes(text)
  children = []
  for text_node in text_nodes:
    html_node = text_node.to_html()
    children.append(html_node)
  return children

def extract_title(markdown):
  if not markdown.startswith("# "):
    raise Exception("Markdown does not start with a level 1 heading")
  end_of_line = markdown.find("\n")
  if end_of_line == -1:
    title = markdown[2:].strip()
  else:
    title = markdown[2:end_of_line].strip()
  return title