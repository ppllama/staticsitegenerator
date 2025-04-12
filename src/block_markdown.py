from enum import Enum

def markdown_to_blocks(md_document):
    blocks = []
    for block in md_document.strip("\n").split("\n\n"):
        if block:
            blocks.append(block.strip())
    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def block_to_block_type(block):
    list_of_lines = block.split("\n")  
    if block.startswith(("# ","## ","### ","#### ","##### ","###### ")):
        return BlockType.HEADING
    # if block.startswith("```") and block.endswith("```"):
    if len(list_of_lines) > 1 and list_of_lines[0].startswith("```") and list_of_lines[-1].startswith("```"):
        return BlockType.CODE
    if all(line.startswith((">"))for line in list_of_lines):
        return BlockType.QUOTE
    if all(line.startswith(("- "))for line in list_of_lines):
        return BlockType.ULIST
    count = 1
    for line in list_of_lines:
        if not line.startswith(f"{count}. "):
            break
        else:
            count += 1
    else:
        return BlockType.OLIST
        
    return BlockType.PARAGRAPH