class CallTree(object):

    def __init__(self, node, parent=None):

        self.call_id = int(node.get('id'))
        self.region_id = int(node.get('calleeId'))
        self.metrics = {}

        self.children = []
        self.parent = parent

        self.state = None
        self.cidx = None

        #cube.cindex[int(node.get('id'))] = self

        #for child_node in node.findall('cnode'):
        #    child_tree = CallTree(child_node, cube)
        #    self.children.append(child_tree)
