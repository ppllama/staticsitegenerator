import unittest

from textnode import TextNode, TextType, text_node_to_html_node

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

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_link(self):
        node = TextNode("papi's website", TextType.LINK, url= "shippy.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "papi's website")
        self.assertEqual(html_node.props, {"href":"shippy.com"})

    def test_text_image(self):
        node = TextNode("papi's website", TextType.IMAGE, url= "shippy.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertNotEqual(html_node.value, "papi's website")
        self.assertEqual(html_node.props, {"src":"shippy.com", "alt":"papi's website"})

    def test_text_invalid(self):
        class MockTextNode:
            def __init__(self):
                self.text = "mock text"
                self.text_type = "INVALID_TYPE"
        
        mock_node = MockTextNode()
        
        with self.assertRaises(ValueError) as context:
            html_node = text_node_to_html_node(mock_node)
        
        self.assertTrue("invalid text type" in str(context.exception))

if __name__ == "__main__":
    unittest.main()
