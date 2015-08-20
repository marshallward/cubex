class CallTree(object):

    def __init__(self, node, cube):

        self.region_id = node.get('calleeId')
        self.children = []

        cube.cindex[int(node.get('id'))] = self

        for child_node in node.findall('cnode'):
            child_tree = CallTree(child_node, cube)
            self.children.append(child_tree)
