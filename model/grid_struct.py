#!/usr/bin/python

import sys
sys.path.append("/Users/tsupinie/lib")

import numpy as np
from geopy import distance

earth_radius = 6371000.

def makeCubicGnomic(face_nx, face_ny):
    coords_lat = np.zeros((6, face_nx, face_ny))
    coords_lon = np.zeros((6, face_nx, face_ny))

    face_x = np.linspace(-(float(face_nx) - 1) / 2, (float(face_nx) - 1) / 2, face_nx) * 2 * earth_radius / face_nx
    face_y = np.linspace(-(float(face_ny) - 1) / 2, (float(face_ny) - 1) / 2, face_ny) * 2 * earth_radius / face_ny

    rad = np.sqrt(face_x.reshape((face_nx, 1)).repeat(face_ny, axis=1) ** 2 + face_y.reshape((1, face_ny)).repeat(face_nx, axis=0) ** 2 + earth_radius ** 2)

    coords_lat[0,:,:] = np.pi / 2 - np.arccos(face_y.reshape((1, face_ny)).repeat(face_nx, axis=0) / rad)
    coords_lon[0,:,:] = np.arctan2(face_x.reshape((face_nx, 1)).repeat(face_ny, axis=1), earth_radius)

    coords_lat[1,:,:] = coords_lat[0,:,:]
    coords_lon[1,:,:] = np.arctan2(earth_radius, -face_x.reshape((face_nx, 1)).repeat(face_ny, axis=1))

    coords_lat[2,:,:] = coords_lat[0,:,:]
    coords_lon[2,:,:] = np.arctan2(-face_x.reshape((face_nx, 1)).repeat(face_ny, axis=1), -earth_radius)

    coords_lat[3,:,:] = coords_lat[0,:,:]
    coords_lon[3,:,:] = np.arctan2(-earth_radius, face_x.reshape((face_nx, 1)).repeat(face_ny, axis=1))

    coords_lat[4,:,:] = np.pi / 2 - np.arccos(earth_radius / rad)
    coords_lon[4,:,:] = np.arctan2(face_y.reshape((1, face_ny)).repeat(face_nx, axis=0), face_x.reshape((face_nx, 1)).repeat(face_ny, axis=1))

    coords_lat[5,:,:] = -coords_lat[4,:,:]
    coords_lon[5,:,:] = coords_lon[4,:,:]

    return {'lat':coords_lat * 180 / np.pi, 'lon':coords_lon * 180 / np.pi}

def main():
    face_size = 200
    coords = makeCubicGnomic(face_nx=face_size, face_ny=face_size)

#   print np.hypot(*np.gradient(2 * (2 * np.pi / 86400) * np.sin(coords['lat']))[1:])

    lat = np.zeros((4 * face_size,))
    dist = np.zeros((4 * face_size,))

    for f, face in enumerate([0, 4, 1, 5]):
        for idx in xrange(face_size):
            face2 = face
            idx2 = idx + 1

            if idx == face_size - 1:
                idx2 = 0
                if face == 5:
                    face2 = 0
                else:
                    face2 = face + 1
 
            lat1 = coords['lat'][face,  (face_size - 1) / 2, idx ]
            lat2 = coords['lat'][face2, (face_size - 1) / 2, idx2] 
            lon1 = coords['lon'][face,  (face_size - 1) / 2, idx ]
            lon2 = coords['lon'][face2, (face_size - 1) / 2, idx2]

            lat[f * 100 + idx] = lat1
            dist[f * 100 + idx] = distance.distance((lat1, lon1), (lat2, lon2)).km

#   for idx in xrange(4 * face_size):
#      print lat[idx], dist[idx]

if __name__ == "__main__":
    main()
