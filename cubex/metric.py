import struct

class Metric(object):

    def __init__(self, node):
        self.name = node.find('uniq_name').text
        self.idx = int(node.get('id'))
        self.display_name = node.find('disp_name').text
        self.description = node.find('descr').text

        self.mtype = node.get('type')           # Metric type
        self.dtype = node.find('dtype').text    # Data type (Do I need this?)
        self.units = node.find('uom').text
        self.url = node.find('url').text

        self.index = None

        # Data file
        self.datafile = None

    def read_index(self, m_index):
        header = m_index.read(11)
        assert header == b'CUBEX.INDEX'

        scratch = m_index.read(7)
        raw_size = m_index.read(4)
        n_nodes = struct.unpack('i', raw_size)[0]

        raw_index = m_index.read(4 * n_nodes)
        self.index = struct.unpack('{}i'.format(n_nodes), raw_index)

    def read(self):
        header = datafile.read(10)
        assert header == b'CUBEX.DATA'
