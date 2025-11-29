import unittest
from textnode import TextNode, TextType
from inline_markdown import extract_markdown_images, extract_markdown_links

class TestExtractors(unittest.TestCase):
  def test_extract_markdown_images(self):
    text = "Here is an image ![alt text](http://example.com/image.png) in the text."
    expected_images = [("alt text", "http://example.com/image.png")]
    images = extract_markdown_images(text)
    self.assertEqual(images, expected_images)

  def test_extract_markdown_links(self):
    text = "Here is a link [link text](http://example.com) in the text."
    expected_links = [("link text", "http://example.com")]
    links = extract_markdown_links(text)
    self.assertEqual(links, expected_links)

  def test_extract_multiple_markdown_images(self):
    text = "Image one ![first](http://example.com/first.png) and image two ![second](http://example.com/second.png)."
    expected_images = [("first", "http://example.com/first.png"), ("second", "http://example.com/second.png")]
    images = extract_markdown_images(text)
    self.assertEqual(images, expected_images)

  def test_extract_multiple_markdown_links(self):
    text = "Link one [first](http://example.com/first) and link two [second](http://example.com/second)."
    expected_links = [("first", "http://example.com/first"), ("second", "http://example.com/second")]
    links = extract_markdown_links(text)
    self.assertEqual(links, expected_links)

  def test_invalid_markdown_image(self):
    text = "This is an invalid image ![alt text(http://example.com/image.png)."
    expected_images = []
    images = extract_markdown_images(text)
    self.assertEqual(images, expected_images)
    
  def test_invalid_markdown_link(self):
    text = "This is an invalid link [link text(http://example.com)."
    expected_links = []
    links = extract_markdown_links(text)
    self.assertEqual(links, expected_links)