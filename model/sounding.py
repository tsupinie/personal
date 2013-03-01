
import numpy as np

class Sounding:
    def __init__(self, file_name, missing_value=-9999.0):
        data_found = False
        fields = ['pres', 'hght', 'temp', 'dwpt', 'wdir', 'wspd']
        dtypes = [float, float, float, float, float, float]

        self._data = {}
        for field in fields:
            self._data[field] = []

        for line in open(file_name, 'r'):
            line = line.strip()
            if data_found:
                if line == "%END%":
                    data_found = False
                    continue

                level = line.split()
                for field, value, dtype in zip(fields, level, dtypes):
                    if value[-1] == ',':
                        value = value[:-1]
                    self._data[field].append(dtype(value))

            else:
                if line == "%RAW%":
                    data_found = True

        for field in fields:
            self._data[field] = np.ma.array(self._data[field], mask=(np.array(self._data[field]) == missing_value))

        return

    def __getitem__(self, key):
        return self._data[key]

if __name__ == "__main__":
    s = Sounding("/Users/tsupinie/Documents/20110410_00Z_KOAX_snd.txt")
    print s['temp']
