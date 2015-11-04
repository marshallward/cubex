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
        self.cubex_file = None

        self.version = None
        self.attrs = {}
        self.docs = None

        self.metrics = {}
        self.regions = {}

        self.calltrees = []
        self.cindex = []

        self.systems = []
        self.locations = []

    def parse(self, cubex_path):

        # Open the .cubex tar file and preserve the reference
        self.cubex_file = tarfile.open(cubex_path, 'r')

        try:
            anchor_file = self.cubex_file.extractfile('anchor.xml')
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
        # TODO: Other profilers (e.g. scalasca) store metrics as trees
        # TODO: This needs to be a function shared by other elements
        for mnode in root.find('metrics').findall('metric'):
            # Old implementation
            #self.metrics.append(Metric(mnode))

            metric = Metric(mnode)
            assert metric.name != metric.idx
            assert metric.name not in self.metrics
            assert metric.idx not in self.metrics

            self.metrics[metric.name] = metric
            self.metrics[metric.idx] = metric

        # Read the metric index
        for name, metric in self.metrics.items():
            index_fname = '{}.index'.format(metric.idx)
            try:
                m_index = self.cubex_file.extractfile(index_fname)
            except KeyError:
                print('{} not found; skipping.'.format(index_fname))
                continue

            metric.read_index(m_index)

        # Regions
        for rnode in root.find('program').findall('region'):
            # Old implementation
            #self.regions.append(Region(rnode))

            region = Region(rnode)
            assert region.name != region.idx
            assert region.idx not in self.regions

            if region.name in self.regions:
                print(region.name, region.idx, self.regions[region.name])
            if region.name in self.regions:
                rlist = self.regions[region.name]
                if not isinstance(rlist, list):
                    rlist = [rlist]
                rlist.append(region)
                self.regions[region.name] = rlist
            else:
                self.regions[region.name] = region

            self.regions[region.idx] = region

        # Call tree
        for cnode in root.find('program').findall('cnode'):
            self.calltrees.append(CallTree(cnode, self))

        # Construct the call tree index
        for ctree in self.calltrees:
            self.cindex.append(ctree)
            ctree.update_index(self.cindex)

        # Location groups
        # TODO: Connect nodes to processes
        #       This is just a dump of the info
        for snode in root.find('system').findall('systemtreenode'):
            self.systems.append(SystemNode(snode))

            for nnode in snode.findall('systemtreenode'):
                for lnode in nnode.findall('locationgroup'):
                    self.locations.append(LocationGroup(lnode))

        # TODO: Topologies

    def read_data(self, metric):

        # Populate data
        # TODO: Get data size (bytes send/recv seems different)
        try:
            m_data_fname = '{}.data'.format(metric.idx)
            print(m_data_fname)
            m_data = self.cubex_file.extractfile(m_data_fname)
        except KeyError:
            # TODO: Fill missing entries with zeros
            pass

        # Skip header
        header = m_data.read(10)
        assert header == b'CUBEX.DATA'

        m_fmt = metric_fmt[metric.dtype]

        for cnode in self.cindex:
            n_bytes = len(self.locations) * 8
            raw = m_data.read(n_bytes)

            fmt = '<' + m_fmt * len(self.locations)
            cnode.metrics[metric.name] = struct.unpack(fmt, raw)


# Taken from CubeMetric.cpp
metric_fmt = {
    'INT8':                 'b',
    'UINT8':                'c',
    'CHAR':                 'c',
    'INT16':                'h',
    'SIGNED SHORT INT':     'h',
    'SHORT INT':            'h',
    'UINT16':               'H',
    'UNSIGNED SHORT INT':   'H',
    'INT32':                'i',
    'SIGNED INT':           'i',
    'INT':                  'i',
    'UINT32':               'I',
    'UNSIGNED INT':         'I',
    'INT64':                'q',
    'SIGNED INTEGER':       'q',
    'INTEGER':              'q',
    'UINT64':               'Q',
    'UNSIGNED INTEGER':     'Q',
    'DOUBLE':               'd',
    'FLOAT':                'd',
    'COMPLEX':              'dd',
    'TAU_ATOMIC':           'P',
    'MINDOUBLE':            'd',
    'MAXDOUBLE':            'd',
    'RATE':                 'P',
    'SCALE_FUNC':           'P',
    'HISTOGRAM':            'P',
    'NDOUBLES':             'P'
}
