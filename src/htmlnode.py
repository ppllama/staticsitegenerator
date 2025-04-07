

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplemented
    
    def props_to_html(self):
        html_string = ""
        if self.props is None or len(self.props) < 1:
            return html_string
        else:
            for key, value in self.props.items():            
                html_string += f' {key}="{value}"'
            return html_string
        
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Leafs must have value")
        if self.tag is None:
            return f"{self.value}"
        if not self.props:
            # Self Note: This catches both None and empty dict
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("parents must have tag")
        if not self.children:
            raise ValueError("Parents must have children")
        else:
            children_copy = self.children.copy()
            string_of_children = ""
            def joiner(children_copy):
                nonlocal string_of_children
                if not children_copy:
                    return string_of_children
                else:
                    string_of_children += (children_copy.pop(0).to_html())
                return joiner(children_copy)
            
            if not self.props:
            # Self Note: This catches both None and empty dict
                return f"<{self.tag}>{joiner(children_copy)}</{self.tag}>"
            else:
                return f"<{self.tag}{self.props_to_html()}>{joiner(children_copy)}</{self.tag}>"