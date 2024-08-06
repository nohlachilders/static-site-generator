import unittest
from htmlnode import *
from textnode import *
from nodeconversions import *


class TestHTMLNode(unittest.TestCase):
    def test_htmlprops(self):
        htmlnode1 = HTMLNode(tag="a", value="body text", props={"href":"https://www.google.com"})
        self.assertEqual(htmlnode1.props_to_html(), " href=\"https://www.google.com\"")

        htmlnode2 = HTMLNode(tag="a", value="body text")
        self.assertEqual(htmlnode2.props_to_html(), "")

        htmlnode3 = HTMLNode(tag="a", value="body text", props={"href":"https://www.google.com", "target":"_blank"})
        self.assertEqual(htmlnode3.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")

    def test_init(self):
        htmlnode1 = HTMLNode(tag="a", value="body text", props={"href":"https://www.google.com"})
        self.assertEqual(htmlnode1.children, None)

        htmlnode2 = HTMLNode()
        for property_name, property_value in vars(htmlnode2).items():
            self.assertEqual(property_value, None)

    def test_eq(self):
        htmlnode1 = HTMLNode(tag="a", value="body text", props={"href":"https://www.google.com"})
        htmlnode2 = HTMLNode(tag="a", value="body text", props={"href":"https://www.google.com"})
        self.assertEqual(htmlnode1, htmlnode2)
        
        htmlnode3 = HTMLNode(tag="a", value="bodysdfasdf text", props={"href":"https://www.google.com"})
        htmlnode4 = HTMLNode(tag="a", value="body text", props={"href":"https://www.google.com"})
        self.assertNotEqual(htmlnode3, htmlnode4)


class TestLeafNode(unittest.TestCase):
    def test_tohtml(self):
        leafnode = LeafNode(tag="a", value="body text", props={"href":"https://www.google.com", "target":"_blank"})
        self.assertEqual(leafnode.to_html(), "<a href=\"https://www.google.com\" target=\"_blank\">body text</a>")

    def test_value(self):
        leafnode = LeafNode(tag="a", props={})
        self.assertRaises(ValueError, leafnode.to_html)

    def test_iseq(self):
        leafnode = LeafNode(tag="a", value="body text", props={"href":"https://www.google.com", "target":"_blank"})
        leafnode2 = LeafNode(tag="a", value="body text", props={"href":"https://www.google.com", "target":"_blank"})
        self.assertEqual(leafnode, leafnode2)

class TestParentNode(unittest.TestCase):
    def test_tohtml(self):
        node1 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        node2 = ParentNode(
                "div",
                [
                    LeafNode("h1", "a heading"),
                    node1,
                    LeafNode(None, "normal stuff"),
                    node1
                ],
            )
        node3 = ParentNode(
                "",
                [
                    LeafNode(None, "some text"),
                ],
                )
        node4 = ParentNode(
                "p",
                [
                ],
                )


        self.assertEqual(node1.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
        self.assertRaises(ValueError, node3.to_html)
        self.assertRaises(ValueError, node4.to_html)

class TestTextToHTMLNode(unittest.TestCase):
    def test_conversion(self):
        textnode = TextNode("link text", "link", "https://www.google.com")
        leafnode = LeafNode(tag="a", value="link text", props={"href":"https://www.google.com"})
        self.assertEqual(text_node_to_html_node(textnode), leafnode)

        textnode2 = TextNode("body text", "", "stuff")
        self.assertRaises(ValueError, text_node_to_html_node, textnode2)

        textnode3 = TextNode("image alt text", "image", "https://www.google.com")
        leafnode3 = LeafNode(tag="img", value="", props={"src":"https://www.google.com","alt":"image alt text"})
        self.assertEqual(text_node_to_html_node(textnode), leafnode)

        textnode4 = TextNode("body text", "text")
        leafnode4 = LeafNode(tag=None, value="body text")
        self.assertEqual(text_node_to_html_node(textnode), leafnode)

class TestSplitDelimiter(unittest.TestCase):
    def test_split(self):
        test_set = [TextNode("hello *bro* how are *you* doing", "text")]
        self.assertEqual(split_nodes_delimiter(test_set, "*", "bold"), [
            TextNode("hello ", "text", None), TextNode("bro", "bold", None), TextNode(" how are ", "text", None),
            TextNode("you", "bold", None), TextNode(" doing", "text", None)
            ])

        test_set2 = [TextNode("hello *bro how are *you* doing", "text")]
        self.assertRaises(ValueError, split_nodes_delimiter, test_set2, "*", "bold")

        test_set3 = [TextNode("hello **bro** how are **you** doing", "text")]
        self.assertEqual(split_nodes_delimiter(test_set3, "**", "bold"), [
            TextNode("hello ", "text", None), TextNode("bro", "bold", None), TextNode(" how are ", "text", None),
            TextNode("you", "bold", None), TextNode(" doing", "text", None)
            ])

        test_set4 = [TextNode("hello **bro** how are **you** doing", "italic"), TextNode("fine **bro** how are you?", "text")]
        #print(split_nodes_delimiter(test_set4, "**", "bold"))
        self.assertEqual(split_nodes_delimiter(test_set4, "**", "bold"), [
            TextNode("hello **bro** how are **you** doing", "italic", None), TextNode("fine ", "text", None), 
            TextNode("bro", "bold", None), TextNode(" how are you?", "text", None)
            ])

class TestRegexLinkExtraction(unittest.TestCase):
    def test_extract(self):
        set1 = extract_markdown_images("![asdfs](asdfsddf),![isdfidf](gdfgdi)")
        self.assertEqual(set1, [("asdfs","asdfsddf"),("isdfidf","gdfgdi")])
        set2 = extract_markdown_images("![](),![]()")
        self.assertEqual(set2, [("",""),("","")])

        set3 = extract_markdown_links("[asdfs](asdfsddf),[isdfidf](gdfgdi)")
        self.assertEqual(set3, [("asdfs","asdfsddf"),("isdfidf","gdfgdi")])
        set4 = extract_markdown_links("[](),[]()")
        self.assertEqual(set4, [("",""),("","")])

    def test_extract_node_images(self):
        set1 = split_nodes_images([TextNode("text ![alt](link), more text ![anoterh alt](link also), and omre text at the end","text")])
        result1 = [TextNode("text ", "text", None), TextNode("alt", "image_link", "link"), TextNode(", more text ", "text", None), TextNode("anoterh alt", "image_link", "link also"), TextNode(", and omre text at the end", "text", None)]
        self.assertEqual(set1, result1)

        set2 = split_nodes_images([TextNode("![alt](link), more text ![](link also), and omre text at the end","text")])
        result2 = [TextNode("alt", "image_link", "link"), TextNode(", more text ", "text", None), TextNode(", and omre text at the end", "text", None)]
        self.assertEqual(set2, result2)

        set3 = split_nodes_images([TextNode("![](),![]()","text")])
        self.assertEqual(set3, [TextNode(",","text")])

    def test_extract_node_links(self):
        set1 = split_nodes_links([TextNode("text [alt](link), more text [anoterh alt](link also), and omre text at the end","text")])
        result1 = [TextNode("text ", "text", None), TextNode("alt", "link", "link"), TextNode(", more text ", "text", None), TextNode("anoterh alt", "link", "link also"), TextNode(", and omre text at the end", "text", None)]
        self.assertEqual(set1, result1)

        set2 = split_nodes_links([TextNode("[alt](link), more text [](link also), and omre text at the end","text")])
        result2 = [TextNode("alt", "link", "link"), TextNode(", more text ", "text", None), TextNode(", and omre text at the end", "text", None)]
        self.assertEqual(set2, result2)

        set3 = split_nodes_links([TextNode("[](),[]()","text")])
        self.assertEqual(set3, [TextNode(",","text")])

    def test_extract_both(self):
        set1 = split_nodes_links(split_nodes_images([TextNode("text [alt](link), more text ![image now](link also), and omre text at the end","text")]))
        #print(set1)
        #ok just know that images must be split before links

class TestTextToTextNodes(unittest.TestCase):
    def tests(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://)"
        #print(text_to_textnode(text))
        result = [
                TextNode("This is ", "text"),
                TextNode("text", "bold"),
                TextNode(" with an ", "text"),
                TextNode("italic", "italic"),
                TextNode(" word and a ", "text"),
                TextNode("code block", "code"),
                TextNode(" and an ", "text"),
                TextNode("obi wan image", "image_link", "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", "text"),
                TextNode("link", "link", "https://"),
                ]
        self.assertEqual(text_to_textnode(text), result)

        text2 = "This is *text* with an **italic** word and a `code block` and an [obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a ![link](https://)"
        #print(text_to_textnode(text))
        result2 = [
                TextNode("This is ", "text"),
                TextNode("text", "italic"),
                TextNode(" with an ", "text"),
                TextNode("italic", "bold"),
                TextNode(" word and a ", "text"),
                TextNode("code block", "code"),
                TextNode(" and an ", "text"),
                TextNode("obi wan image", "link", "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", "text"),
                TextNode("link", "image_link", "https://"),
                ]
        self.assertEqual(text_to_textnode(text), result)


if __name__ == "__main__":
    unittest.main()
