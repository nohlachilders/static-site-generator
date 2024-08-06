from textnode import *
from htmlnode import *
import nodeconversions

def main():
    node1 = TextNode("hello", "jello")
    node2 = TextNode("hello", "jello")

    htmlnode1 = HTMLNode(tag="a", value="body text", props={"href":"https://www.google.com"})
    print(node1)
    print(node1 == node2)
    print(htmlnode1)

main()
