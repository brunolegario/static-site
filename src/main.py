from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []
  for node in old_nodes:
    if node.text_type != TextType.PLAIN:
      new_nodes.append(node)
    
    if delimiter not in node.text:
      new_nodes.append(node)
      continue

    split_node = node.text.split(delimiter)
    if len(split_node) < 3:
      raise Exception("invalid markdown syntax")
    
    for i in range(len(split_node)):
      if split_node[i] == "":
        continue
      if i % 2 == 0:
        new_nodes.append(TextNode(split_node[i], TextType.PLAIN))
      else:
        new_nodes.append(TextNode(split_node[i], text_type))
    
  return new_nodes

def main():
  # node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
  # print(node)

  node = TextNode("This is text with a `code block` word", TextType.PLAIN)
  new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

main()