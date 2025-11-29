import os
import sys
import shutil
from textnode import TextNode, TextType
from inline_markdown import text_to_textnodes
from blocktype import markdown_to_html_node, extract_title

def copy_static_to_public():
  src_dir = os.path.join(os.path.dirname(__file__), '..', 'static')
  dest_dir = os.path.join(os.path.dirname(__file__), '..','docs')

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

def generate_page(from_path, template_path, dest_path, basepath):
  print(f"Generating page from {from_path} to {dest_path} using template {template_path}")

  with open(from_path, 'r') as f:
    content = f.read()

  with open(template_path, 'r') as f:
    template = f.read()

  html_content = markdown_to_html_node(content).to_html()
  title = extract_title(content)

  template = template.replace("{{ Title }}", title)
  template = template.replace("{{ Content }}", html_content)
  template = template.replace('href="/', f"href=\"{basepath}")
  template = template.replace('src="/', f"src=\"{basepath}")

  dest_dir = os.path.dirname(dest_path)
  if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

  with open(dest_path, 'w') as f:
    f.write(template)

def generate_pages(content_path, template_path, destination_path, basepath):
  for item in os.listdir(content_path):
    src_path = os.path.join(content_path, item)
    
    if os.path.isdir(src_path):
      dest_path = os.path.join(destination_path, item)
      generate_pages(src_path, template_path, dest_path, basepath)

    elif item.endswith('.md'):
      html_filename = item.replace('.md', '.html')
      dest_path = os.path.join(destination_path, html_filename)
      generate_page(src_path, template_path, dest_path, basepath)



def main():
  args = sys.argv
  
  basepath = "/"
  if args[1]:
    basepath = args[1]

  copy_static_to_public()
  
  script_dir = os.path.dirname(__file__)
  content_dir = os.path.join(script_dir, '..', 'content')
  template_path = os.path.join(script_dir, '..', 'template.html')
  public_dir = os.path.join(script_dir, '..', 'docs')
  
  generate_pages(content_dir, template_path, public_dir, basepath)
main()