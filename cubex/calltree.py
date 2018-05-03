class CallTree(object):

    def __init__(self, node, cube, parent=None):

        self.idx = int(node.get('id'))
        self.metrics = {}

        region_id = int(node.get('calleeId'))
        self.region = cube.rindex[region_id]

        # Append the cnode to the corresponding region
        self.cube = cube
        cube.rindex[region_id].cnodes.append(self)

        self.parent = parent
        self.children = []

        # Construct the inclusive and exclusive index maps
        # These may be breadth-first and depth-first, respectively, but my
        # memory is that they are similar, but not identical, to them.
        cube.exclusive_index.append(self.idx)

        for child_node in node.findall('cnode'):
            child_tree = CallTree(child_node, cube, self)
            self.children.append(child_tree)

    def update_index(self, index):
        self.cube.inclusive_index.extend([c.idx for c in self.children])

        index[self.idx] = self
        for child in self.children:
            child.update_index(index)

    def print_tree(self, indent=''):
        print(indent + '- ' + self.region.name)
        for child in self.children:
            child.print_tree(indent + '  ')
