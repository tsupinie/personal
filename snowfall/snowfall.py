
import numpy as np

from scipy.interpolate import griddata

import matplotlib
matplotlib.use('agg')
import pylab
from matplotlib.delaunay import delaunay
from mpl_toolkits.basemap import Basemap

from datetime import datetime, timedelta
from math import floor

def loadReports(file_name):
    dtype=[("station_id", '|S12'), ('station_name', '|S30'), ('latitude', float), ('longitude', float), ('elevation', int), ('physical_element', '|S10'), 
        ('report_time', datetime), ('amount', float), ('amount_units', '|S5'), ('duration', float), ('duration_units', '|S5'), ('zip_code', int)]

    converter = {
        4: lambda e: int(e.split(" ")[0]),
        6: lambda t: datetime.strptime(t, "%Y-%m-%d %H:%M"),
        11: lambda z: 99999 if z == "" else int(z)
    }

    reports = np.loadtxt(file_name, dtype=dtype, delimiter="|", comments="!", converters=converter, skiprows=2, usecols=range(len(dtype)))
    
    return reports

def findAvgStationSpacing(stn_xs, stn_ys):
    centers, edges, triangles, neighbors = delaunay(stn_xs, stn_ys)
    dists = np.hypot(stn_xs[edges[:, 0]] - stn_xs[edges[:, 1]], stn_ys[edges[:, 0]] - stn_ys[edges[:, 1]])
    return dists.mean()

def main():
    buffer_width=40000
    reports = loadReports("snowfall_2013022600_m.txt")
#   map = Basemap(projection='lcc', resolution='i', area_thresh=10000.,
#                 llcrnrlat=20., llcrnrlon=-120., urcrnrlat=48., urcrnrlon=-60.,
#                 lat_0=34.95, lon_0=-97.0, lat_1=30., lat_2=60.)

    map = Basemap(projection='lcc', resolution='i', area_thresh=10000.,
                  llcrnrlat=25., llcrnrlon=-110., urcrnrlat=40., urcrnrlon=-90.,
                  lat_0=34.95, lon_0=-97.0, lat_1=30., lat_2=60.)

    width, height = map(map.urcrnrlon, map.urcrnrlat)
    report_xs, report_ys = map(reports['longitude'], reports['latitude'])

    keep_idxs = np.where((report_xs >= -buffer_width) & (report_xs <= width + buffer_width) & (report_ys >= -buffer_width) & (report_ys <= height + buffer_width))

    spacing = findAvgStationSpacing(*map(reports['longitude'][keep_idxs], reports['latitude'][keep_idxs]))

    dx = dy = floor(spacing * 0.75 / 2000) * 2000
    print dx, dy
    xs, ys = np.meshgrid(np.arange(0, width, dx), np.arange(0, height, dy))

    grid = griddata((report_xs[keep_idxs], report_ys[keep_idxs]), reports['amount'][keep_idxs], (xs, ys))

    pylab.contourf(xs, ys, grid / 2.54, levels=np.arange(2, 22, 2), cmap=pylab.cool())
    pylab.colorbar(orientation='horizontal')

    map.drawcoastlines()
    map.drawcountries()
    map.drawstates()
    pylab.savefig("snow.png")
    return

if __name__ == "__main__":
    main()
