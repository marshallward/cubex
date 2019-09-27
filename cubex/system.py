class System(object):
    def __init__(self, node, cube):
        self.nodes = []
        for snode in node.findall('systemtreenode'):
            self.nodes.append(SystemNode(snode, cube))


class SystemNode(object):
    def __init__(self, node, cube):
        self.name = node.find('name').text
        self.node_class = node.find('class').text
        self.node_id = node.attrib['Id']

        self.attrs = {}
        self.nodes = []
        self.locationgroups = []

        for attr in node.findall('attr'):
            self.attrs[attr.attrib['key']] = attr.attrib['value']

        for snode in node.findall('systemtreenode'):
            self.nodes.append(SystemNode(snode, cube))

        for locgrp in node.findall('locationgroup'):
            self.locationgroups.append(LocationGroup(locgrp))


class LocationGroup(object):
    def __init__(self, node):
        self.name = node.find('name').text
        self.rank = int(node.find('rank').text)
        self.loc_type = node.find('type').text
        self.loc_id = node.attrib['Id']

        self.locations = []

        for loc in node.findall('location'):
            self.locations.append(Location(node.find('location')))


class Location(object):
    def __init__(self, node):
        self.name = node.find('name').text
        self.rank = int(node.find('rank').text)
        self.loc_type = node.find('type').text
        self.loc_id = node.attrib['Id']
