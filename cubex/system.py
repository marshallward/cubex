class System(object):
    def __init__(self, node):
        self.nodes = []

        # Storing locationgroups and locations at toplevel
        # NOTE: Not sure this is what I want to do yet...
        self.locationgroups = []
        self.locations = []

        for snode in node.findall('systemtreenode'):
            self.nodes.append(SystemNode(snode, self))


class SystemNode(object):
    def __init__(self, node, system):
        self.name = node.find('name').text
        self.node_class = node.find('class').text
        self.node_id = node.attrib['Id']

        self.attrs = {}
        self.nodes = []
        self.locationgroups = []

        for attr in node.findall('attr'):
            self.attrs[attr.attrib['key']] = attr.attrib['value']

        for snode in node.findall('systemtreenode'):
            self.nodes.append(SystemNode(snode, system))

        for locgrp_node in node.findall('locationgroup'):
            locgrp = LocationGroup(locgrp_node, system)
            self.locationgroups.append(locgrp)
            system.locationgroups.append(locgrp)


class LocationGroup(object):
    def __init__(self, node, system):
        self.name = node.find('name').text
        self.rank = int(node.find('rank').text)
        self.grp_type = node.find('type').text
        self.grp_id = node.attrib['Id']

        self.locations = []

        for loc_node in node.findall('location'):
            loc = Location(loc_node)
            self.locations.append(loc)
            system.locations.append(loc)


class Location(object):
    def __init__(self, node):
        self.name = node.find('name').text
        self.rank = int(node.find('rank').text)
        self.loc_type = node.find('type').text
        self.loc_id = node.attrib['Id']
