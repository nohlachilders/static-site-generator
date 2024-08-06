import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("text", "bold", "stuff.com")
        node2 = TextNode("text", "bold", "stuff.com")
        self.assertEqual(node, node2)
    
    def test_url(self):
        node = TextNode("text", "none")
        self.assertEqual(node.url, None)

    def test_type(self):
        node = TextNode("text", "bold")
        node2 = TextNode("text", "italic")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
