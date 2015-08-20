class SystemNode(object):

    def __init__(self, node):
        self.name = node.find('name').text
        self.sclass = node.find('class').text


class Location(object):

    def __init__(self, node):
        self.name = node.find('name').text
        self.rank = int(node.find('rank').text)
        self.ltype = node.find('type').text


class LocationGroup(Location):

    def __init__(self, node):

        super(LocationGroup, self).__init__(node)
        self.locations = []

        for loc in node.findall('location'):
            self.locations.append(Location(node.find('location')))
