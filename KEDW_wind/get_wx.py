#!/usr/bin/python

import urllib
import numpy as np

def download(file_name):
    params = {'ls_baseLayers':'Google Streets',
              'CA_ASOS Network':'CA_ASOS Network',
              'station':'EDW',
              'data':'all',

              'month1':'5',
              'day1':'1',
              'month2':'5',
              'day2':'31',

              'tz':'GMT',
              'format':'comma',
              'latlon':'no'
             }

    lines = []

    for year in range(1941, 2011):
        print year
        params['year1'] = str(year)
        params['year2'] = str(year)

        param_str = urllib.urlencode(params)
        f = urllib.urlopen("http://mesonet.agron.iastate.edu/cgi-bin//request/getData.py?%s" % param_str)

        lines.extend(f.read().strip().split('\n'))

    f = open(file_name, 'w')
    f.write("\n".join(lines))
    f.close()

def parse(file_name):
    ws = []
    f = open(file_name, 'r')
    for line in f:
        data = line.split(',')
        if data[6] not in ['M']:
            ws.append(float(data[6]))
    f.close()

    ws = np.array(ws)
    print ws

    thresholds = [5, 10, 15, 20, 25, 30, 35, 40]
    for t in thresholds:
        number = len(np.where(ws >= t)[0])
        print "Percentage over %d knots: %f" % (t, float(number) / len(ws))

def main():
    get = False
    file_name = "EDW_wx.txt"

    if get:
        download(file_name)
    parse(file_name)

if __name__ == "__main__":
    main()
