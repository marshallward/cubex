__version__ = '0.0a'

from cubex.cube import Cube

def read(cube_path):
    """Create a CUBE object."""
    cube = Cube()
    cube.parse(cube_path)
    return cube
