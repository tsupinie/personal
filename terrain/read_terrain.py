
import numpy as np
import struct

byte_string = ""
with open("w060n90.Bathymetry.srtm", 'r') as file:
    byte_string = file.read()

print byte_string[-20:]

byte_list = np.array(struct.unpack('h' * (len(byte_string) / 2), byte_string[:-1]))
print byte_list.min()
print byte_list.max()    
