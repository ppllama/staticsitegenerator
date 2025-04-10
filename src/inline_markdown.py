from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_node = []
        sequence = old_node.text.split(delimiter)
        if len(sequence) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")

        for i in range(len(sequence)):
            if sequence[i] == "":
                continue
            if i % 2 != 0:
                split_node.append(TextNode(sequence[i], text_type))
            if i % 2 == 0:
                split_node.append(TextNode(sequence[i], TextType.TEXT))
        new_nodes.extend(split_node)
    return new_nodes