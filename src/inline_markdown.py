import re
from textnode import TextNode, TextType

def extract_markdown_images(text):
  pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
  matches = re.findall(pattern, text)
  return matches

  # images = []
  # parts = text.split("![")

  # for part in parts[1:]:
  #   alt_text_end = part.find("]")
  #   if alt_text_end == -1:
  #     continue
  #   alt_text = part[:alt_text_end]

  #   url_start = part.find("(", alt_text_end)
  #   url_end = part.find(")", url_start)
  #   if url_start == -1 or url_end == -1:
  #     continue
  #   url = part[url_start+1 : url_end]

  #   images.append((alt_text, url))

  # return images

def extract_markdown_links(text):
  pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
  matches = re.findall(pattern, text)
  return matches

  # links = []
  # parts = text.split("[")

  # for part in parts[1:]:
  #   link_text_end = part.find("]")
  #   if link_text_end == -1:
  #     continue
  #   link_text = part[:link_text_end]

  #   url_start = part.find("(", link_text_end)
  #   url_end = part.find(")", url_start)
  #   if url_start == -1 or url_end == -1:
  #     continue
  #   url = part[url_start+1 : url_end]

  #   links.append((link_text, url))

  # return links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []
  for node in old_nodes:
    if node.text_type != TextType.PLAIN:
      new_nodes.append(node)
      continue
    
    if delimiter not in node.text:
      new_nodes.append(node)
      continue

    temp_text = node.text
    while delimiter in temp_text:
      parts = temp_text.split(delimiter, 2)
      if len(parts) < 3:
        raise Exception("invalid markdown syntax")

      if parts[0] and parts[0] != "":
        new_nodes.append(TextNode(parts[0], TextType.PLAIN))
      new_nodes.append(TextNode(parts[1], text_type))
      temp_text = parts[2]

    if temp_text and temp_text != "":
      new_nodes.append(TextNode(temp_text, TextType.PLAIN))

    # split_node = node.text.split(delimiter)
    # if len(split_node) < 3:
    #   raise Exception("invalid markdown syntax")
    
    # for i in range(len(split_node)):
    #   if split_node[i] == "":
    #     continue
    #   if i % 2 == 0:
    #     new_nodes.append(TextNode(split_node[i], TextType.PLAIN))
    #   else:
    #     new_nodes.append(TextNode(split_node[i], text_type))
    
  return new_nodes

def split_nodes_image(old_nodes):
  new_nodes = []
  for node in old_nodes:
    if node.text_type != TextType.PLAIN:
      new_nodes.append(node)
      continue

    images = extract_markdown_images(node.text)
    if not images:
      new_nodes.append(node)
      continue

    temp_text = node.text
    for alt_text, url in images:
      markdown_image = f"![{alt_text}]({url})"
      parts = temp_text.split(markdown_image, 1)
      if parts[0]:
        new_nodes.append(TextNode(parts[0], TextType.PLAIN))
      new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
      temp_text = parts[1]
    
    if temp_text and temp_text != "":
      new_nodes.append(TextNode(temp_text, TextType.PLAIN))

  return new_nodes

def split_nodes_link(old_nodes):
  new_nodes = []
  for node in old_nodes:
    if node.text_type != TextType.PLAIN:
      new_nodes.append(node)
      continue

    links = extract_markdown_links(node.text)
    if not links:
      new_nodes.append(node)
      continue

    temp_text = node.text
    for link_text, url in links:
      markdown_link = f"[{link_text}]({url})"
      parts = temp_text.split(markdown_link, 1)
      if parts[0]:
        new_nodes.append(TextNode(parts[0], TextType.PLAIN))
      new_nodes.append(TextNode(link_text, TextType.LINK, url))
      temp_text = parts[1]
    
    if temp_text and temp_text != "":
      new_nodes.append(TextNode(temp_text, TextType.PLAIN))

  return new_nodes

def text_to_textnodes(text):
  nodes = []
  if type(text) is str:
    nodes = [TextNode(text, TextType.PLAIN)]
  elif type(text) is TextNode:
    nodes = [text]
  
  nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
  nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
  nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
  nodes = split_nodes_image(nodes)
  nodes = split_nodes_link(nodes)
  
  return nodes

