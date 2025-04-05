import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_different_names(self):
        node = TextNode("This is the first text", TextType.ITALIC)
        node2 = TextNode("This is the second text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_different_url(self):
        node = TextNode("This is a text node", TextType.CODE, "booty.dev")
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node,node2)

if __name__ == "__main__":
    unittest.main()
