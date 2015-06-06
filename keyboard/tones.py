
import numpy as np
import struct
from datetime import datetime, timedelta
import wave

class Tone(object):
    pitches = [ 'C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B' ]

    def __init__(self, pitch, volume, rate=44100):
        self._pitch = pitch
        self._vol = volume
        self._freq = Tone.pitch2Freq(pitch)

        self._rate = rate
        self._n_sample = 0

        self._dt_max = np.iinfo(np.int16).max
        self._dt_min = np.iinfo(np.int16).min

    def generate(self, size):
        samples = np.arange(self._n_sample, self._n_sample + size)
        audio = self._vol * np.sin(2 * np.pi * samples * self._freq / self._rate)

        dt_mag = (self._dt_max - self._dt_min + 1) / 2
        dt_off = self._dt_min + dt_mag
        dt_audio = (dt_mag * audio + dt_off).astype(np.int16)

        self._n_sample += size
        return dt_audio

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
    def __init__(self, fundamental, harmonics):
        self._fund = fundamental
        self._harm = harmonics

        for intv, loudness in self._harm.iteritems():
            pass

    def generate(self, size):
        pass

    def __eq__(self, other):
        is_eq = False
        if type(other) == Note:
            is_eq = (self._fund == other._fund)
        return is_eq

    def __neq__(self, other):
        return not self.__eq__(other)

class NoteGenerator(object):
    def __init__(self):
        self._notes = []
        self._wave_data = []

    def addNote(self, pitch):
        self._notes.append(pitch)

    def removeNote(self, pitch):
        if pitch in self._notes:
            self._notes.remove(pitch)

    def generate(self, size=512):
        chunks = [ n.generate(size) for n in self._notes ]
        mixed = NoteGenerator.mix(chunks, [ 0.25 for c in chunks ], size)
        self._wave_data.append(mixed)
        return NoteGenerator.render(mixed)

    def writeToFile(self, file_name):
        RATE = 44100
        WIDTH = 2
        CHANNELS = 1

        dat = NoteGenerator.render(np.concatenate(tuple(self._wave_data)))

        wf = wave.open(file_name, 'w')
        wf.setparams((CHANNELS, WIDTH, RATE, 0, 'NONE', 'not compressed'))
        wf.writeframes(dat)
        wf.close()

    @staticmethod
    def mix(chunks, vols, size):
        mixed = np.zeros((size,))
        for ch, vl in zip(chunks, vols):
            mixed += (vl * ch)
        return mixed

    @staticmethod
    def render(ary_data):
        n_samples = len(ary_data)
        data = struct.pack("%dh" % n_samples, *ary_data)
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

    tones = [
        Tone('C5', 0.25),
        Tone('E5', 0.25),
        Tone('G5', 0.25),
    ]

    gen = NoteGenerator()

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
                gen.addNote(tones[note_idx])
                note_idx += 1
        except KeyboardInterrupt:
            print
            break

    print "done"

    stream.stop_stream()
    stream.close()

    p.terminate()
