import tarfile
import xml.etree.ElementTree as ElementTree

from cubex.metric import Metric
from cubex.region import Region

class Cube(object):

    def __init__(self):
        self.version = None
        self.attrs = {}
        self.docs = None

        self.metrics = []
        self.regions = []
        self.system = None

    def parse(self, cubex_path):

        # Open the .cubex tar file and preserve the reference
        cubex = tarfile.open(cubex_path, 'r')

        try:
            anchor_file = cubex.extractfile('anchor.xml')
        except KeyError:
            # TODO: exit gracefully
            print('cubex: error: anchor.xml file not in {0}.'
                  ''.format(cubex_path))
            raise

        anchor = ElementTree.parse(anchor_file)
        root = anchor.getroot()

        assert root.tag == 'cube'
        self.version = root.attrib['version']

        # Attributes
        self.attrs = {}
        for n in root.iter('attr'):
            self.attrs[n.attrib['key']] = n.attrib['value']

        # Docs
        # TODO

        # Metrics
        for m in root.find('metrics').iter('metric'):
            self.metrics.append(Metric(m))

        # Regions
        for r in root.find('program').iter('region'):
            self.regions.append(Region(r))
