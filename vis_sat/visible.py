## (C) Kelton Halbert 2012
#!/usr/bin/env python
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap, interp
import matplotlib.pyplot as plt
import numpy as np


def plotMap(x, y, vis, map, file_name):
    plt.clf()
    cmap = plt.cm.gist_gray

    map.drawcoastlines()
    map.drawcountries()
    map.drawstates()
    map.pcolor( x, y, vis, cmap=cmap )
    plt.colorbar( orientation='horizontal' )

    plt.savefig(file_name)
    return

stride = 8
data_thin = slice(None, None, stride)

## Load the data from the morthelode server
d = Dataset( 'http://motherlode.ucar.edu/thredds/dodsC/satellite/VIS/EAST-CONUS_1km/current/EAST-CONUS_1km_VIS_20121125_2001.gini' )

## Load the satellite projection
m = Basemap( llcrnrlon=-113.1333, llcrnrlat=16.3691, urcrnrlon=-68.286995, urcrnrlat=63.109997, projection='lcc', resolution='i', area_thresh=1000, rsphere=6371229.0, lat_1=25., lat_0=25., lon_0=-95. )

## Convert the x and y coordinates from kilometers to meters
x = d.variables[ 'x' ][data_thin]*1000
y = d.variables[ 'y' ][data_thin]*1000
## "nudge" the arrays so that x.min becomes 0 and y.min becomes 0
x = x + -1*x.min()
y = y + -1*y.min()

xs, ys = np.meshgrid(x, y)

vis = d.variables[ 'VIS' ][ 0 ][data_thin, data_thin]

plotMap(xs, ys, vis, m, "visible.png")

lons, lats = m( xs, ys, inverse=True )

n = Basemap(width=5000000,height=3000000,
            rsphere=6371229.0,\
            resolution='i',area_thresh=1000.,projection='lcc',\
            lat_1=40,lat_2=30,lat_0=38.5,lon_0=-98.5)

x_new, y_new = n( lons, lats )

## plot away
plotMap(x_new, y_new, vis, n, "visible_new.png")
