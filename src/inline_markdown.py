from textnode import TextNode, TextType
import re

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

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if not old_node:
            continue
        images = extract_markdown_images(old_node.text)
        if not images:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        for i in range(len(images)):
            splited = text.split(f"![{images[i][0]}]({images[i][1]})",1)
            if splited[0]:
                new_nodes.append(TextNode(splited[0], TextType.TEXT))
            new_nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
            text = splited[1]
        if text:
            new_nodes.append(TextNode(text,TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if not old_node:
            continue
        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        for i in range(len(links)):
            splited = text.split(f"[{links[i][0]}]({links[i][1]})",1)
            if splited[0]:
                new_nodes.append(TextNode(splited[0], TextType.TEXT))
            new_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
            text = splited[1]
        if text:
            new_nodes.append(TextNode(text,TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes