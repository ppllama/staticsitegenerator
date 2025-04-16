from textnode import *
import os, shutil
from pathlib import Path

from block_markdown import (
    markdown_to_html_node,
    extract_title
)


def main():
    copy_to_public()
    from_path = "content"
    template_path = "template.html"
    dest_path = "public"
    generate_pages_recursive(from_path, template_path, dest_path)

def copy_to_public():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    public_dir = os.path.join(script_dir, "../public")
    static_dir = os.path.join(script_dir, "../static")

    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    os.mkdir(public_dir)

    def copier(from_dir, to_dir):
        object_list = os.listdir(from_dir)
        for object in object_list:
            source_path = os.path.join(from_dir, object)
            dest_path = os.path.join(to_dir, object)
            if os.path.isfile(source_path):
                print(f"copying file: {source_path}")
                shutil.copy(source_path,dest_path)
            else:
                print(f"copying directory: {source_path}")
                os.makedirs(dest_path, exist_ok=True)
                copier(source_path,dest_path)
    
    copier(static_dir,public_dir)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as md_file:
        markdown = md_file.read()
    with open(template_path, 'r') as tpl_file:
        template = tpl_file.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as output_file:
        output_file.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Generating website from {dir_path_content} to {dest_dir_path} using {template_path}")
    dir_path_content = Path(dir_path_content)
    dest_dir_path = Path(dest_dir_path)
    object_list = dir_path_content.iterdir()

    for object in object_list:
        source_path = dir_path_content / object.name
        dest_path = dest_dir_path / object.name

        if source_path.is_file():
            if source_path.suffix == ".md":
                print(f"making and copying html: {source_path}")
                dest_path = dest_path.with_suffix(".html")
                generate_page(source_path, template_path, dest_path)
            else:
                print(f"Skipping invalid file format: {source_path}")
                continue
        elif source_path.is_dir():
            print(f"copying directory: {source_path}")
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(source_path, template_path, dest_path)

main()