from textnode import *
from htmlnode import *
import re

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case "text":
            return LeafNode(None, text_node.text)
        case "bold":
            return LeafNode("b", text_node.text)
        case "italic":
            return LeafNode("i", text_node.text)
        case "code":
            return LeafNode("code", text_node.text)
        case "link":
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case "image":
            return LeafNode("img", "", {"src":f"{text_node.url}", "alt":{text_node.text}})
        case _:
            raise ValueError("Invalid format for text node! Is the tag a valid tag?")

def split_nodes_delimiter(old_nodes, delimiter, text_type) -> list:
    new_nodes = []
    for i in old_nodes:
        if i.text_type != "text":
            new_nodes.append(i)
            continue
        i_strings = i.text.split(delimiter)
        if len(i_strings) % 2 == 0:
            raise ValueError("Markdown delimiter not closed")
        for j in range(0, len(i_strings)):
            match j % 2:
                case 0:
                    new_nodes.append(TextNode(i_strings[j], i.text_type))
                case 1:
                    new_nodes.append(TextNode(i_strings[j], text_type))

    return new_nodes

def extract_markdown_images(text):
    textlist = re.findall(r"!\[(.*?)\]\((.*?)\)" ,text)
    return textlist

def extract_markdown_links(text):
    textlist = re.findall(r"\[(.*?)\]\((.*?)\)" ,text)
    return textlist

def split_nodes_images(old_nodes) -> list:
    new_nodes = []

    for i in old_nodes:
        working_text = i.text
        extracted_images = extract_markdown_images(i.text)
        match extracted_images:
            case ():
                new_nodes.append(i)
            case _:
                for link in extracted_images:
                    i_sections = working_text.split(f"![{link[0]}]({link[1]})", 1)
                    #print(i_sections)
                    if (i_sections[0] != ""):
                        new_nodes.append(TextNode(i_sections[0], i.text_type))
                    if (link[0] != ""):
                        new_nodes.append(TextNode(link[0], "image_link", link[1]))
                    working_text = i_sections[-1]
                if working_text != "":
                    new_nodes.append(TextNode(working_text, i.text_type))
      
    return new_nodes

def split_nodes_links(old_nodes) -> list:
    new_nodes = []

    for i in old_nodes:
        working_text = i.text
        extracted_links = extract_markdown_links(i.text)
        match extracted_links:
            case ():
                new_nodes.append(i)
            case _:
                for link in extracted_links:
                    i_sections = working_text.split(f"[{link[0]}]({link[1]})", 1)
                    #print(i_sections)
                    if (i_sections[0] != ""):
                        new_nodes.append(TextNode(i_sections[0], i.text_type))
                    if (link[0] != ""):
                        new_nodes.append(TextNode(link[0], "link", link[1]))
                    working_text = i_sections[-1]
                if working_text != "":
                    new_nodes.append(TextNode(working_text, i.text_type))
      
    return new_nodes

def text_to_textnode(text):
    text_nodes = [TextNode(text, "text")]
    types = {
            "bold":"**",
            "italic":"*",
            "code":"`"
            }

    for text_type, delimiter in types.items():
        text_nodes = split_nodes_delimiter(text_nodes, delimiter, text_type)

    text_nodes = split_nodes_images(text_nodes)
    text_nodes = split_nodes_links(text_nodes)

    return text_nodes

def markdown_to_blocks(markdown:str) -> list:
    blocks = markdown.split("\n\n")

    blocks = [i for i in blocks if i != ""]
    blocks = [i.strip() for i in blocks]

    return blocks

def block_to_block_type(block) -> str:
    if re.search("^#{1,6} ", block):
        return "header"

    if re.search("^(```)[\s\S]*(```)$", block):
        return "code"

    quote = True
    for line in block.splitlines():
        if not re.search("^>", line):
            quote = False
    if quote:
        return "quote"

    unordered_list = True
    for line in block.splitlines():
        if not re.search("^[*-] ", line):
            unordered_list = False
    if unordered_list:
        return "unordered_list"

    ordered_list = True
    list_count = 1
    for line in block.splitlines():
        if not re.search(f"^{list_count}\. ", line):
            ordered_list = False
        list_count += 1
    if ordered_list:
        return "ordered_list"
    
    return "paragraph"
