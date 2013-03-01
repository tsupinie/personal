import struct
import cPickle

import matplotlib
matplotlib.use('agg')
import pylab
from matplotlib.patches import Polygon

from mpl_toolkits.basemap import Basemap

from visited import visited

_fips = """
AK  02  ALASKA
AL  01  ALABAMA
AR  05  ARKANSAS
AS  60  AMERICAN SAMOA
AZ  04  ARIZONA
CA  06  CALIFORNIA
CO  08  COLORADO
CT  09  CONNECTICUT
DC  11  DISTRICT OF COLUMBIA
DE  10  DELAWARE
FL  12  FLORIDA
GA  13  GEORGIA
GU  66  GUAM
HI  15  HAWAII
IA  19  IOWA
ID  16  IDAHO
IL  17  ILLINOIS
IN  18  INDIANA
KS  20  KANSAS
KY  21  KENTUCKY
LA  22  LOUISIANA
MA  25  MASSACHUSETTS
MD  24  MARYLAND
ME  23  MAINE
MI  26  MICHIGAN
MN  27  MINNESOTA
MO  29  MISSOURI
MP  69  NORTHERN MARIANA ISLANDS
MS  28  MISSISSIPPI
MT  30  MONTANA
NC  37  NORTH CAROLINA
ND  38  NORTH DAKOTA
NE  31  NEBRASKA
NH  33  NEW HAMPSHIRE
NJ  34  NEW JERSEY
NM  35  NEW MEXICO
NV  32  NEVADA
NY  36  NEW YORK
OH  39  OHIO
OK  40  OKLAHOMA
OR  41  OREGON
PA  42  PENNSYLVANIA
PR  72  PUERTO RICO
RI  44  RHODE ISLAND
SC  45  SOUTH CAROLINA
SD  46  SOUTH DAKOTA
TN  47  TENNESSEE
TX  48  TEXAS
UT  49  UTAH
VA  51  VIRGINIA
VI  78  VIRGIN ISLANDS
VT  50  VERMONT
WA  53  WASHINGTON
WI  55  WISCONSIN
WV  54  WEST VIRGINIA
WY  56  WYOMING
"""

class DBF(object):

    _fips_state_name = dict([ tuple([f[4:6], f[8:]]) for f in _fips.split('\n') ])
    _fips_state_abbrev = dict([ tuple([f[4:6], f[:2]]) for f in _fips.split('\n') ])

    def __init__(self, file_name):
        self._dbf = open(file_name, 'r')
        self._readHeaders()
        self._readRecords()
        return

    def _readHeaders(self):
        file_type = self._read('b')
        last_update = self._read('b' * 3)
        self._num_records = self._read('i')
        first_record_pos = self._read('h')
        record_length = self._read('h')
        self._read('b' * 20)

        num_fields = (first_record_pos - 33) / 32

        self._fields = []
        for n_field in range(num_fields):
            field = {}

            field['name'] = self._read('s10')
            field['type'] = self._read('b')
            field['displacement'] = self._read('i')
            field['length'] = self._read('b')
            field['precision'] = self._read('b')
            self._read('b' * 15)

            self._fields.append(field)

        self._read('b')
        return

    def _readRecords(self):
        self._records = []
        for n_record in range(self._num_records):
            record = {}
            delete_char = self._read('c')
            for field in self._fields:
                record[field['name']] = self._read('s' + str(field['precision'])).strip()

            record['STATENAME'] = DBF._fips_state_name[record['STATEFP']]
            record['STATEABBRV'] = DBF._fips_state_abbrev[record['STATEFP']]

            if delete_char == ' ':
                self._records.append(record)
            else:
                print "Ignoring %s, %s ..." % (record['NAME'], record['STATENAME'])
        return

    def _read(self, type_string):
        if type_string[0] != 's':
            size = struct.calcsize(type_string)
            data = struct.unpack("<%s" % type_string, self._dbf.read(size))
        else:
            size = int(type_string[1:])
            data = tuple([ self._dbf.read(size).strip("\0") ])

        if len(data) == 1:
            return data[0]
        else:
            return list(data)

    def search(self, counties, abbrev=True):
        indexes = []
        for n_record, record in enumerate(self._records):
            for (county, state) in counties:
                if (abbrev and state == record['STATEABBRV'] or not abbrev and state == record['STATENAME']) and county == record['NAME']:
                    indexes.append(n_record)
        return indexes

def main():
    # Lambert Conformal map of USA lower 48 states
    map = Basemap(projection='lcc', resolution='i', 
        llcrnrlon=-119, llcrnrlat=22, urcrnrlon=-64, urcrnrlat=49,
        lat_1=33, lat_2=45, lon_0=-95, area_thresh=10000)

    dbf = cPickle.load(open('counties.pkl', 'r'))
    indexes = dbf.search(visited)

    pylab.figure(figsize=(10, 8))
    pylab.axes((0, 0, 1, 1))

#   map.readshapefile("/data6/tsupinie/tl_2009_us_county", 'county')

    for idx, record in enumerate(dbf._records):
        color = 'none'
        if idx in indexes:
            color = '#008800'

        pylab.gca().add_patch(Polygon(record['boundary'], fc=color))

    map.drawcoastlines()
    map.drawcountries()
    map.drawstates()

    pylab.savefig("counties.png")

    return

if __name__ == "__main__":
    main()
