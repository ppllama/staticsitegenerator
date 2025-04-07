import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={
        "href": "https://www.google.com",
        "target": "_blank",
        })
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
        print(node)
    
    def test_props_to_html_empty(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), '')

    def test_constructor(self):
        node = HTMLNode("div", "content", [], {"class":"container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "content")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class":"container"})
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Link to my Website!", {"href": "https://www.boot.dev/lessons/ac96cd47-bf01-4599-8291-cd69534f288f"})
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev/lessons/ac96cd47-bf01-4599-8291-cd69534f288f">Link to my Website!</a>')

    def test_leaf_to_html_b_not_equal(self):
        node = LeafNode("b", "Bold text", {"class": "important"})
        self.assertNotEqual(node.to_html(), "<b>Bold text</b>")


if __name__ == "__main__":
    unittest.main()
