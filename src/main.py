import os
import shutil
from textnode import TextNode, TextType
from inline_markdown import text_to_textnodes
from blocktype import markdown_to_html_node

def copy_static_to_public():
  src_dir = os.path.join(os.path.dirname(__file__), '..', 'static')
  dest_dir = os.path.join(os.path.dirname(__file__), '..','public')

  if os.path.exists(dest_dir):
    shutil.rmtree(dest_dir)
  
  os.mkdir(dest_dir)
  
  copy_files(src_dir, dest_dir)

def copy_files(src, dest):
  if not os.path.exists(dest):
    os.mkdir(dest)
  
  for item in os.listdir(src):
    src_path = os.path.join(src, item)
    dest_path = os.path.join(dest, item)
    
    if os.path.isdir(src_path):
      copy_files(src_path, dest_path)
    else:
      shutil.copy2(src_path, dest_path)
      print(f"Copied: {src_path} -> {dest_path}")

def main():
  copy_static_to_public()

main()