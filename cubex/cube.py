import collections
import struct
import tarfile
import xml.etree.ElementTree as ElementTree

from cubex.metric import Metric
from cubex.region import Region
from cubex.calltree import CallTree
from cubex.system import SystemNode, Location, LocationGroup

class Cube(object):

    def __init__(self):
        self.version = None
        self.attrs = {}
        self.docs = None

        self.metrics = []
        self.regions = []
        self.calltrees = []
        self.cindex = []

        self.systems = []
        self.locations = []

    def parse(self, cubex_path):

        # Open the .cubex tar file and preserve the reference
        cubex = tarfile.open(cubex_path, 'r')

        try:
            anchor_file = cubex.extractfile('anchor.xml')
        except KeyError:
            # TODO: Exit gracefully
            raise

        anchor = ElementTree.parse(anchor_file)
        root = anchor.getroot()

        assert root.tag == 'cube'
        self.version = root.attrib['version']

        # Attributes
        self.attrs = {}
        for anode in root.findall('attr'):
            self.attrs[anode.attrib['key']] = anode.attrib['value']

        # Docs
        # TODO

        # Metrics
        for mnode in root.find('metrics').findall('metric'):
            self.metrics.append(Metric(mnode))

        # Regions
        for rnode in root.find('program').findall('region'):
            self.regions.append(Region(rnode))

        # Call tree index (BFS implementation)
        for ctree in root.find('program').findall('cnode'):
            bfs_tree = collections.deque([ctree])
            while bfs_tree:
                ctree_xnode = bfs_tree.popleft()
                bfs_tree.extend(ctree_xnode)
                self.cindex.append(CallTree(ctree_xnode))

        # Location groups
        # TODO: Connect nodes to processes
        #       This is just a dump of the info
        for snode in root.find('system').findall('systemtreenode'):
            self.systems.append(SystemNode(snode))

            for nnode in snode.findall('systemtreenode'):
                for lnode in nnode.findall('locationgroup'):
                    self.locations.append(LocationGroup(lnode))

        # TODO: Topologies

        # Populate data
        # TODO: Get data size (bytes send/recv seems different)
        for m_id, metric in enumerate(self.metrics[:4]):

            try:
                m_data = cubex.extractfile('{}.data'.format(m_id))
            except:
                # TODO: Fill missing entries with zeros
                continue

            # Skip header
            header = m_data.read(10)
            assert header == 'CUBEX.DATA'

            m_fmt = metric_fmt[metric.dtype]

            for cnode in self.cindex:
                n_bytes = len(self.locations) * 8
                raw = m_data.read(n_bytes)

                fmt = '<' + m_fmt * len(self.locations)
                cnode.metrics[metric.name] = struct.unpack(fmt, raw)


metric_fmt = {'UINT64': 'Q',
              'DOUBLE': 'd',
              'MAXDOUBLE': 'd',
              'MINDOUBLE': 'd',
             }
