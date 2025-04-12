import unittest

from block_markdown import (
    BlockType,
    markdown_to_blocks,
    block_to_block_type
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




if __name__== "__main__":
    unittest.main()