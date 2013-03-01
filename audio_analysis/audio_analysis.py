
import numpy as np

import struct

sample_rate = 44100.
base_pitch = 440
base_factor = base_pitch * 2 * np.pi
base_octave = 6

def loadAudio(file_name, n_channels=1):
    file = open(file_name, 'r')
    input = file.read()
    file.close()

    raw_audio = struct.unpack("<" + "l" * (len(input) / 4), input)
    audio = []
    for idx in range(n_channels):
        audio.append(np.array([ sample for jdy, sample in enumerate(raw_audio) if not ((jdy - idx) % n_channels) ]))
    return tuple(audio)

def getMultiplier(pitch):
    pitches = {'A':0, 'B':2, 'C':-9, 'D':-7, 'E':-5, 'F':-4, 'G':-2}
    octave = int(pitch[-1])
    note = pitch[:-1]

    note_diff = pitches[note[0]]
    if len(note) == 2:
        if note[1] == "b": note_diff -= 1
        else:              note_diff += 1

    pitch_factor = 2 ** ((octave - base_octave) + note_diff / 12.)

    return pitch_factor

def getNoteName(freq, prefer='b'):
    notes_flat = [ 'A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab' ]
    notes_sharp = [ 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#' ]
    semitones_from_base = int(np.round_(np.log2(freq / 440) * 12))
    octave = base_octave + semitones_from_base / 12
    if prefer == 'b':
        return "%s%d" % (notes_flat[semitones_from_base % 12], octave)
    elif prefer == '#':
        return "%s%d" % (notes_sharp[semitones_from_base % 12], octave)
    return

def findComponent(wave, pitch):
    time = np.arange(len(wave)) / sample_rate

    amplitude = max(wave.max(), abs(wave.min()))
    pitch_factor = getMultiplier(pitch)

    tone = np.round_(amplitude * np.sin(base_factor * pitch_factor * time)).astype(np.int32)
    return wave / float(amplitude), tone / float(amplitude), (tone / float(amplitude)) * (wave / float(amplitude))

def main():
    waves = loadAudio("mars.intro.rawaudio", n_channels=2)
    audio = waves[0]

    spectrum = np.fft.fft(audio)[:len(audio) / 2]
    freqs = np.fft.fftfreq(len(audio), d=(1. / sample_rate))[:len(audio) / 2]

    freq_spectrum = zip(freqs, spectrum)[1:]
    freq_spectrum.sort(cmp=lambda x, y: cmp(np.abs(x[1]), np.abs(y[1])), reverse=True)

    for idx in range(20):
        print getNoteName(freq_spectrum[idx][0])

#   comp = findComponent(wave[0], "Gb5")
#   file = open("raw.txt", 'w')
#   for f, a, p in zip(freqs, spectrum, spectrum): file.write("%f, %f, %f\n" % (f, np.abs(a), np.angle(p)))
#   file.close()
    return

if __name__ == "__main__":
    main()
