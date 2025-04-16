import unittest

from block_markdown import (
    BlockType,
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    extract_title
)

class TestBlockMarkdown(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_simple_paragraph(self):
        block = "This is a simple paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_heading_single_hash(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_multiple_hashes(self):
        block = "###### This is a heading level 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        
    def test_heading_with_additional_lines(self):
        block = "# This is a heading\nThis is a paragraph after the heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_code_block_simple(self):
        block = "```\ncode line\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        
    def test_code_block_with_language(self):
        block = "```python\ndef hello():\n    print('Hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_quote_block_simple(self):
        block = ">This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        
    def test_quote_block_multiple_lines(self):
        block = ">Line 1\n>Line 2\n>Line 3"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_unordered_list_simple(self):
        block = "- Item 1"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
    
    def test_unordered_list_multiple_items(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
    
    def test_ordered_list_simple(self):
        block = "1. Item 1"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
    
    def test_ordered_list_multiple_items(self):
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
    
    def test_ordered_list_incorrect_order(self):
        # This should be a paragraph because 2 doesn't follow 1
        block = "1. Item 1\n3. Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    # Edge cases
    def test_empty_block(self):
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_almost_heading(self):
        # Missing space after #
        block = "#This is not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_almost_code_block(self):
        # Only has opening backticks
        block = "```\ncode line"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_almost_quote_block(self):
        # One line doesn't start with >
        block = ">Line 1\nLine 2\n>Line 3"

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_extract_title(self):
        md = "# smegma"
        title = extract_title(md)
        self.assertEqual("smegma", title)

    def test_leading_whitespace(self):
        md = "   #    Gandalf  "
        with self.assertRaises(ValueError):
            extract_title(md)
    
    def test_multiple_titles(self):
        md = "# First Title\n# Second Title"
        title = extract_title(md)
        self.assertEqual("First Title", title)  # Should return the first title

    def test_no_title(self):
        md = "This is some text\nNo title here"
        with self.assertRaises(ValueError):
            extract_title(md)


if __name__== "__main__":
    unittest.main()