import numpy as np

from sounding import Sounding

class AtmosphereState:
    def __init__(self, **kwargs):
        nx = kwargs['nx']
        ny = kwargs['ny']

        if 'nz' in kwargs:
            nz = kwargs['nz']
        else:
            nz = 1

        if 'ne' in kwargs:
            ne = kwargs['ne']
        else:
            ne = 1

        self._u  = np.zeros((nx, ny, nz, ne))
        self._v  = np.zeros((nx, ny, nz, ne))
        self._w  = np.zeros((nx, ny, nz, ne))
        self._pt = np.zeros((nx, ny, nz, ne))
        self._gp = np.zeros((nx, ny, nz, ne))
        self._qv = np.zeros((nx, ny, nz, ne))

        if kwargs['initialization'] == 'sounding':
            

        return

    def advance(self):
        return

if __name__ == "__main__":
    s = Sounding("/Users/tsupinie/20110410_00Z_KOAX_snd.txt")

    g = AtmosphereState(
        nx=64, ny=64, nz=36,                                   # Grid dimensions
        center_lat=35.21, center_lon=-97.42, dx=1000, dy=1000, # Grid horizontal location and size
        vertical_coord='pres', dp=5000,                        # Grid vertical configuration

        initialization='sounding', initial_profile=s,          # Initialization 
    )
