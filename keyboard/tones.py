
import numpy as np
import struct
from datetime import datetime, timedelta
import wave

class Tone(object):
    pitches = [ 'C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B' ]

    def __init__(self, pitch, n_channels, bit_rate):
        self._pitch = pitch
        self._freq = Tone.pitch2Freq(pitch)

        self._has_cutoff = False
        self._is_finished = False

        self._rate = bit_rate
        self._n_sample = 0

    def generate(self, size):
        samples = np.arange(self._n_sample, self._n_sample + size)
        audio = np.sin(2 * np.pi * samples * self._freq / self._rate)

        self._n_sample += size
        return audio

    def cutoff(self):
        self._has_cutoff = True
        self._is_finished = True

    def isFinished(self):
        return self._is_finished

    def __eq__(self, other):
        is_eq = False
        if type(other) == Tone:
            is_eq = (self._pitch == other._pitch)
        return is_eq

    def __neq__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def intervalFromC0(pitch):
        if len(pitch) == 4:
            note, octv = pitch[:-2], int(pitch[-2:])
        else:
            note, octv = pitch[:-1], int(pitch[-1:])

        return Tone.pitches.index(note) + len(Tone.pitches) * octv

    @staticmethod
    def intvC0ToPitch(interval):
        octave, note_idx = divmod(interval, len(Tone.pitches))
        return "%s%d" % (Tone.pitches[note_idx], octave)

    @staticmethod
    def pitch2Freq(pitch):
        intv_a440 = Tone.interval('A4', pitch)
        return 440. * 2 ** (intv_a440 / 12.)

    @staticmethod
    def interval(pitch_from, pitch_to):
        intv_from_c0 = Tone.intervalFromC0(pitch_from)
        intv_to_c0 = Tone.intervalFromC0(pitch_to)
        return intv_to_c0 - intv_from_c0

    @staticmethod
    def moveByInterval(pitch, interval):
        intv_c0 = Tone.intervalFromC0(pitch)
        return Tone.intvC0ToPitch(intv_c0 + interval)

class Note(object):
    def __init__(self, fundamental, harmonics, n_channels, bit_rate):
        self._fund = fundamental
        self._harm = harmonics
        self._n_channels = n_channels
        self._bit_rate = bit_rate

        self._tones = []
        self._vols = []

        for intv, loud in self._harm.iteritems():
            harm_pitch = Tone.moveByInterval(self._fund, intv)
            self._tones.append(Tone(harm_pitch, self._n_channels, self._bit_rate))
            self._vols.append(loud)

    def generate(self, size):
        chunks = [ t.generate(size) for t in self._tones ]
        return NoteGenerator.mix(chunks, self._vols, size)

    def cutoff(self):
        for t in self._tones:
            t.cutoff()

    def isFinished(self):
        return all( t.isFinished() for t in self._tones )

    def __eq__(self, other):
        is_eq = False
        if type(other) == Note:
            is_eq = (self._fund == other._fund)
        return is_eq

    def __neq__(self, other):
        return not self.__eq__(other)

class NoteGenerator(object):
    def __init__(self, n_channels, bit_rate, dtype=np.int16):
        self._n_channels = n_channels
        self._dtype = dtype
        self._bit_rate = bit_rate
        self._master_volume = 0.25

        self._harmonics = {0:1.}
        self._notes = []
        self._volumes = []
        self._wave_data = []

    def setTambre(self, harmonics):
        self._harmonics = harmonics

    def setVolume(self, volume):
        self._master_volume = volume

    def addNote(self, pitch, loudness):
        self._volumes.append(loudness)
        self._notes.append(Note(pitch, self._harmonics, self._n_channels, self._bit_rate))

    def removeNote(self, pitch, loudness):
        note = Note(pitch, self._harmonics, self._n_channels, self._bit_rate)
        if note in self._notes:
            idx = self._notes.index(note)
            self._notes[idx].cutoff()

    def generate(self, size=512):
        finished_notes = [ n for n in self._notes if n.isFinished() ]
        for n in finished_notes:
            self._volumes.remove(self._volumes[self._notes.index(n)])
            self._notes.remove(n)

        chunks = [ n.generate(size) for n in self._notes ]
        mixed = self._master_volume * NoteGenerator.mix(chunks, self._volumes, size)
        self._wave_data.append(mixed)
        return NoteGenerator.render(mixed, self._dtype)

    def writeToFile(self, file_name):
        dat = NoteGenerator.render(np.concatenate(tuple(self._wave_data)), self._dtype)

        wf = wave.open(file_name, 'w')
        wf.setparams((self._n_channels, self._dtype.itemsize, self._bit_rate, 0, 'NONE', 'not compressed'))
        wf.writeframes(dat)
        wf.close()

    @staticmethod
    def mix(chunks, vols, size):
        mixed = np.zeros((size,))
        for ch, vl in zip(chunks, vols):
            mixed += (vl * ch)
        return mixed

    @staticmethod
    def render(ary_data, dtype):
        n_samples = len(ary_data)

        dt_max = np.iinfo(dtype).max
        dt_min = np.iinfo(dtype).min

        dt_mag = (dt_max - dt_min + 1) / 2
        dt_off = dt_min + dt_mag
        dt_audio = (dt_mag * ary_data + dt_off).astype(dtype)

        data = struct.pack("%dh" % n_samples, *dt_audio)
        return data

if __name__ == "__main__":
    import pyaudio
    from time import sleep

    RATE = 44100
    RECORD_SECONDS = 5
    CHUNK = 128
    WIDTH = 2
    CHANNELS = 1

    p = pyaudio.PyAudio()

    tones = [ 'C5', 'E5', 'G5' ]

    gen = NoteGenerator(CHANNELS, RATE)

    def grabMore(in_data, frame_count, time_info, status):
        data = gen.generate(frame_count)
        return (data, pyaudio.paContinue)

    stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK,
                stream_callback=grabMore)

    print "playing"
    stream.start_stream()

    note_idx = 0
    while True:
        try:
            sleep(1)
            if note_idx < len(tones):
                gen.addNote(tones[note_idx], 0.25)
                note_idx += 1
        except KeyboardInterrupt:
            print
            break

    print "done"

    stream.stop_stream()
    stream.close()

    p.terminate()
