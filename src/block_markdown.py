

def markdown_to_blocks(md_document):
    blocks = []
    for block in md_document.strip("\n").split("\n\n"):
        if block:
            blocks.append(block.strip())
    return blocks