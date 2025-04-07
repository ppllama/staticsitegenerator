import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={
        "href": "https://www.google.com",
        "target": "_blank",
        })
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    
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
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_without_children(self):
        with self.assertRaises(ValueError) as context:
            parent_node = ParentNode("div", [])
            parent_node.to_html()

        self.assertEqual(str(context.exception), "Parents must have children")

    def test_to_html_multiple_children(self):
        child_node = LeafNode("h1", "googoogaagaa")
        parent_node = ParentNode("p", [child_node, child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<p><h1>googoogaagaa</h1><h1>googoogaagaa</h1></p>",
        )

    def test_to_html_parent_nested(self):
        child_node = LeafNode("h1", "googoogaagaa")
        parent_node = ParentNode("p", [child_node])
        parent_node_2 = ParentNode("b", [parent_node,child_node])
        self.assertEqual(
            parent_node_2.to_html(),
            "<b><p><h1>googoogaagaa</h1></p><h1>googoogaagaa</h1></b>",
        )

    def test_to_html_multiple_props(self):
        child_node = LeafNode("span", "googoogaagaa", {"id": "container", "data-test": "main-content"})
        parent_node = ParentNode("p", [child_node], {"href": "https://example.com", "class": "button", "target": "_blank"})
        self.assertEqual(
            parent_node.to_html(),
            '<p href="https://example.com" class="button" target="_blank"><span id="container" data-test="main-content">googoogaagaa</span></p>',
        )


if __name__ == "__main__":
    unittest.main()
