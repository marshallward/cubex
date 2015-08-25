class CallTree(object):

    def __init__(self, node, parent=None):

        self.call_id = int(node.get('id'))
        self.region_id = int(node.get('calleeId'))
        self.metrics = {}

        self.parent = parent
        self.children = []

        for child_node in node.findall('cnode'):
            child_tree = CallTree(child_node, self)
            self.children.append(child_tree)

    def update_index(self, index):
        index.extend(self.children)
        for child in self.children:
            child.update_index(index)
