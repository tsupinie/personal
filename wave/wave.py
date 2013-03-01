
import numpy as np
from sys import stdout, stderr

sample_rate = 44100
a_440_factor = 440 * 2 * np.pi

tempo = 150
#notes   =    [ -5,  None, -5,  None, -5,  None, None, None, -5, -5, -5, -2, -5, 0  ]
#lengths =    [ 8,   8,    8,   8,    8,   8,    8,    16,   16, 8,  8,  8,  16, 16 ]
#amplitudes = [ 1.0 for l in lengths ]

notes =      [ 0,   3,    7,    12,  7,    3,    0,   5,    9,    12,  9,    5,    0,   3,    7,    12,  7,    3,    0,   5,    9,    12,  9,    5    ]
lengths =    [ 12,  12,   12,   12,  12,   12,   12,  12,   12,   12,  12,   12,   12,  12,   12,   12,  12,   12,   12,  12,   12,   12,  12,   12   ]
amplitudes = [ 1.0, 0.75, 0.75, 1.0, 0.75, 0.75, 1.0, 0.75, 0.75, 1.0, 0.75, 0.75, 1.0, 0.75, 0.75, 1.0, 0.75, 0.75, 1.0, 0.75, 0.75, 1.0, 0.75, 0.75 ]

for pitch, length, amplitude in zip(notes, lengths, amplitudes):
    time = np.arange(0, (4. / length) * 60. / tempo, 1. / sample_rate)
    if pitch is None:
        stdout.write(np.zeros(time.shape).astype(np.int8))
    else:
        pitch_factor = 2 ** (pitch / 12.)

        stdout.write(np.round_(127 * amplitude * np.sin(a_440_factor * pitch_factor * time)).astype(np.int8))
