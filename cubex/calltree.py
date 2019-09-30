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

    def __getitem__(self, index):
        # TODO: Assert integer
        return self.children[index]

    def update_index(self, index):
        self.cube.inclusive_index.extend([c.idx for c in self.children])

        index[self.idx] = self
        for child in self.children:
            child.update_index(index)

    def print_tree(self, indent='', depth=None):
        print(indent + '- ' + self.region.name)

        if depth is not None:
            depth = depth - 1

        if depth is None or depth > 0:
            for child in self.children:
                child.print_tree(indent + '  ', depth=depth)

    def print_weights(self, metric_name, interval=None):
        # TODO: Check that metric is inclusive
        # TODO: Check arguments

        sloc, eloc = interval if interval else (None, None)

        self_sum = sum(self.metrics[metric_name][sloc:eloc])

        weights = {}
        reg_idx = {}
        children_sum = 0.
        for idx, child in enumerate(self.children):
            child_sum = sum(child.metrics[metric_name][sloc:eloc])
            children_sum += child_sum

            weights[child.region.name] = child_sum / self_sum
            reg_idx[child.region.name] = idx

        weights[self.region.name] = (self_sum - children_sum) / self_sum
        reg_idx[self.region.name] = '-'

        for region in sorted(weights, key=weights.get, reverse=True):
            print('{:.3f}: [{}] {}'
                  ''.format(weights[region], reg_idx[region], region))
