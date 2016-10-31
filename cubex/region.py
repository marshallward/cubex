class Region(object):

    def __init__(self, node):
        # FIXME: are these new to 4.4??
        # And what is 4.4 anyway, latest is 4.3.4!!
        #   - mangled_name, paradigm, role

        self.name = node.find('name').text
        self.idx = int(node.get('id'))
        #self.mangled_name = node.find('mangled_name').text
        self.description = node.find('descr').text
        self.url = node.find('url').text

        # Call tree node references
        self.cnodes = []

        # Classification
        #self.paradigm = node.find('paradigm').text
        #self.role = node.find('role').text

        # No idea...
        self.mod = node.get('mod')      # What is this?
        self.begin = node.get('begin')
        self.end = node.get('end')
