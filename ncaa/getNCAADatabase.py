
import urllib, urllib2
import xml.dom.minidom as dom
import cPickle

import os.path

import gc

import matplotlib
matplotlib.use('agg')
import pylab
from mpl_toolkits.basemap import Basemap

map_projection = {
    'projection':'lcc',
    'llcrnrlat':20.9,
    'llcrnrlon':-120.0,
    'urcrnrlat':48.0,
    'urcrnrlon':-60.0,

    'lat_0':34.95,
    'lon_0':-97.0,

    'lat_1':30.0,
    'lat_2':60.0,
    'resolution':'i',
    'area_thresh':10000,
}

state_names = {
    "Alabama":"AL",
    "Alaska":"AK",
    "Arizona":"AZ",
    "Arkansas":"AR",
    "California":"CA",
    "Colorado":"CO",
    "Connecticut":"CT",
    "Delaware":"DE",
    "Florida":"FL",
    "Georgia":"GA",
    "Hawaii":"HI",
    "Idaho":"ID",
    "Illinois":"IL",
    "Indiana":"IN",
    "Iowa":"IA",
    "Kansas":"KS",
    "Kentucky":"KY",
    "Louisiana":"LA",
    "Maine":"ME",
    "Maryland":"MD",
    "Massachusetts":"MA",
    "Michigan":"MI",
    "Minnesota":"MN",
    "Mississippi":"MS",
    "Missouri":"MO",
    "Montana":"MT",
    "Nebraska":"NE",
    "Nevada":"NV",
    "New Hampshire":"NH",
    "New Jersey":"NJ",
    "New Mexico":"NM",
    "New York":"NY",
    "North Carolina":"NC",
    "North Dakota":"ND",
    "Ohio":"OH",
    "Oklahoma":"OK",
    "Oregon":"OR",
    "Pennsylvania":"PA",
    "Rhode Island":"RI",
    "South Carolina":"SC",
    "South Dakota":"SD",
    "Tennessee":"TN",
    "Texas":"TX",
    "Utah":"UT",
    "Vermont":"VT",
    "Virginia":"VA",
    "Washington":"WA",
    "West Virginia":"WV",
    "Wisconsin":"WI",
    "Wyoming":"WY"
}

def loadPlaceDB(file_name):
    full_db = open(file_name, 'r').read()
    db = [ dbl.split("\t") for dbl in full_db.split("\n") ]

    del full_db
    gc.collect()

    db = dict([ ("%s, %s" % (dbl[1], dbl[10]), (float(dbl[4]), float(dbl[5]))) for dbl in db if len(dbl) > 10 ])
    gc.collect()    
    return db

def loadWiki(overwrite=False):
    local_name = "fbs.html"

    if overwrite or not os.path.exists(local_name):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        wikipage = opener.open("http://en.wikipedia.org/wiki/List_of_NCAA_Division_I_FBS_football_programs").read()

        open(local_name, 'w').write(wikipage)
    else:
        wikipage = open(local_name, 'r').read()
    return wikipage

def getText(cell):
    text = []
    for node in cell.childNodes:
        if node.nodeType == node.TEXT_NODE:
            text.append(node.data)
        elif node.childNodes[0].nodeType == node.TEXT_NODE:
            text.append(node.childNodes[0].data)
    return " ".join(text)

def getTable(doc):
    table_root = doc.getElementsByTagName('table')[1]
    table = []
    for row in table_root.childNodes[1:]:
        school = [ ]
        for column in row.childNodes:
            text = getText(column)
            if text == "" and len(column.childNodes) > 0:
                text = getText(column.childNodes[0])

            school.append(text)

        school[5:6] = []
        if school[2] == "Urbana - Champaign":
            school[2] = "Champaign"
        school[2] = "%s, %s" % (school[2], state_names[school[3]])
        school[3:4] = []
        table.append(school)
    return table

def main():
    place_db = loadPlaceDB("/Users/tsupinie/US/US.txt")

    wikipage = loadWiki()
    wikipage_nonewlines = "".join(wikipage.split("\n"))
    wikidom = dom.parseString(wikipage_nonewlines)

    table = getTable(wikidom)

    locs = []
    for school in table:
        print school[2], place_db[school[2]]
        locs.append(place_db[school[2]])

    map = Basemap(**map_projection)
    xs, ys = map(*reversed(zip(*locs)))

    pylab.figure()
    pylab.axes((0, 0, 1, 1))

    pylab.plot(xs, ys, "ko")
    map.drawstates(linewidth=1.0)
    map.drawcountries(linewidth=1.0)
    map.drawcoastlines(linewidth=1.0)

    pylab.savefig("schools.png")
    pylab.close()
    return

if __name__ == "__main__":
    main()
