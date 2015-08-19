class Metric(object):

    def __init__(self, node):
        self.name = node.find('uniq_name').text
        self.display_name = node.find('disp_name').text
        self.description = node.find('descr').text

        self.mtype = node.get('type')           # Metric type
        self.dtype = node.find('dtype').text    # Data type (Do I need this?)
        self.units = node.find('uom').text
        self.url = node.find('url').text

        # TODO: file object to data?
