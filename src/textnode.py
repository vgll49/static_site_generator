from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "TEXT text"
    BOLD = "bold text"
    ITALIC = "italic text"
    CODE = "code text"
    LINK = "link"
    IMAGE = "url"
    

class TextNode: 
    def __init__(self, text, text_type: TextType, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
        
    def __eq__(self, value):
        if not isinstance (value, TextNode):
         return NotImplemented
     
        return self.text == value.text and self.text_type == value.text_type and self.url == value.url
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag= None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b",value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i",value=text_node.text)
        case TextType.LINK:
             return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.CODE:
            return LeafNode(tag="code",value=text_node.text)
        case TextType.IMAGE:
             return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Invalid")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
           # print("first if")

            start_delim = node.text.find(delimiter)
            if start_delim != -1:
                end_delim = node.text.find(delimiter, start_delim + len(delimiter))
                if end_delim != -1:
                    before = node.text[:start_delim]
                    middle = node.text[start_delim + len(delimiter):end_delim]
                    after = node.text[end_delim + len(delimiter):]
                    n = [TextNode(before, TextType.TEXT),TextNode(middle, text_type), (after, TextType.TEXT)]
                    new_nodes.extend(n)
                    print(f"n{n} new nodes list thats extended: {new_nodes}")
            else:
                raise ValueError("Invalid Markdown Syntax. Check the delimiters.")
        else:
            print("ELSE USED")
            new_nodes.append(node)        
    return new_nodes