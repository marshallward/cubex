class CallTree(object):

    def __init__(self, node):

        self.call_id = int(node.get('id'))
        self.region_id = int(node.get('calleeId'))
        self.children = []
        self.metrics = {}

        #cube.cindex[int(node.get('id'))] = self

        #for child_node in node.findall('cnode'):
        #    child_tree = CallTree(child_node, cube)
        #    self.children.append(child_tree)
