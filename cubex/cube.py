import tarfile
import xml.etree.ElementTree as ElementTree

from cubex.metric import Metric
from cubex.region import Region
from cubex.calltree import CallTree

class Cube(object):

    def __init__(self):
        self.version = None
        self.attrs = {}
        self.docs = None

        self.metrics = []
        self.regions = []
        self.calltrees = []
        self.cindex = []

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

        # Call tree counter
        # TODO: Derive this number from file size?
        n_nodes = 0
        for cnode in root.find('program').iter('cnode'):
            n_nodes += 1
        self.cindex = [None] * n_nodes

        for cnode in root.find('program').findall('cnode'):
            self.calltrees.append(CallTree(cnode, self))

        # Populate data
        # TODO
