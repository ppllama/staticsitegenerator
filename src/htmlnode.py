

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplemented
    
    def props_to_html(self):
        print(self.props)
        html_string = ""
        if len(self.props) < 1:
            return html_string
        else:
            for key, value in self.props.items():            
                html_string += f' {key}="{value}"'
            return html_string
        
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"