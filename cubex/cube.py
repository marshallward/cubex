import collections
import struct
import tarfile
import xml.etree.ElementTree as ElementTree

from cubex.metric import Metric
from cubex.region import Region
from cubex.calltree import CallTree
from cubex.system import SystemNode, Location, LocationGroup


class Cube(object):

    # Implementation

    def __init__(self):
        self.cubex_file = None

        self.version = None
        self.attrs = {}
        self.docs = None

        self.metrics = {}
        self.regions = {}
        self.calltrees = []
        self.systems = []
        self.locationgrps = []  # TODO: move locationgroups inside of system

        # Index lookup tables (TODO: phase this out)
        self.rindex = {}
        self.cindex = []

        # User configuration
        self.verbose = False

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    # Public API

    def open(self, path):
        self.cubex_file = tarfile.open(path, 'r')
        self.read_anchor()

    def close(self):
        self.cubex_file.close()

    # Support functions

    def read_anchor(self):
        # NOTE: Using a `with` construct here will fail on Python 2, since
        # tarfile's ExtObject doesn't support __exit__()
        anchor_file = self.cubex_file.extractfile('anchor.xml')
        anchor = ElementTree.parse(anchor_file)
        anchor_file.close()

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
        # TODO: Some profilers (e.g. scalasca) store metrics as trees
        for mnode in root.find('metrics').findall('metric'):
            metric = Metric(mnode)
            self.metrics[metric.name] = metric

        # Read the metric index and get the data file
        for name, metric in self.metrics.items():

            index_fname = '{}.index'.format(metric.idx)
            try:
                m_index = self.cubex_file.extractfile(index_fname)
            except KeyError:
                if self.verbose:
                    print('{} not found; skipping.'.format(index_fname))
                continue

            metric.read_index(m_index)

            # Get the data file object (but do not read)
            try:
                m_data_fname = '{}.data'.format(metric.idx)
                metric.datafile = self.cubex_file.extractfile(m_data_fname)
            except KeyError:
                # TODO: Fill missing entries with zeros
                pass

        # Regions
        for rnode in root.find('program').findall('region'):

            region = Region(rnode)

            if region.name in self.regions:
                rlist = self.regions[region.name]
                if not isinstance(rlist, list):
                    rlist = [rlist]
                rlist.append(region)
                self.regions[region.name] = rlist
            else:
                self.regions[region.name] = region

            self.rindex[region.idx] = region

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
                    self.locationgrps.append(LocationGroup(lnode))

        # TODO: Topologies

    def read_data(self, metric_name):

        metric = self.metrics[metric_name]

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
            n_locs = 0
            for locgrp in self.locationgrps:
                n_locs += len(locgrp.locations)

            n_bytes = n_locs * 8
            raw = m_data.read(n_bytes)

            fmt = '<' + m_fmt * n_locs
            cnode.metrics[metric.name] = struct.unpack(fmt, raw)

    # User interface
    def show_metrics(self):
        for metric in self.metrics.keys():
            print(metric)



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
