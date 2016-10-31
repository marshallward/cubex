__version__ = '0.0a'

from cubex.cube import Cube

def open(path):
    """Create a CUBE object."""
    cube = Cube()
    cube.open(path)
    return cube
