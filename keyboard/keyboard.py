
import usb.core
import pyaudio
from tones import NoteGenerator, Tone
import sys

def playNote(gen, keyNum, loudness):
    pitches = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B' ]
    base = 24
    
    octave, pitch = divmod(keyNum - base, len(pitches))
    note = "%s%d" % (pitches[pitch], octave)
    if loudness > 0:
        gen.addNote(note, loudness / 128.)
    else:
        gen.removeNote(note, loudness / 128.)

def changeVolume(level):
    pass

def pitchBend(amount):
    print "Pitch bend is %.2f" % ((amount - 64) / 64.)

def handleInput(generator, sequence):
    control = list(sequence)[:2]

    if control == [9, 144]:
        keyNum, loudness = sequence[2:]
        playNote(generator, keyNum, loudness)
    elif control == [ 11, 176 ]:
        mod_control = sequence[2]
        if mod_control == 1:
            # Modulation
            pass
        elif mod_control == 7:
            # Volume
            pass
        else:
            print "Unrecognized modulation control code:", mod_control
    elif control == [ 14, 224 ]:
        bend_amount = sequence[3]
        pitchBend(bend_amount)
        pass
    else:
        print "Unrecognized control sequence:", control

def setupUSB():
    dev = usb.core.find(idVendor=0x763, idProduct=0x192)
    dev.set_configuration()

    intf = dev[0][1, 0]

    endpoint_addr = intf[0].bEndpointAddress

    dev.read_ = dev.read
    dev.read = lambda nb: dev.read_(endpoint_addr, nb, interface=intf)
    return dev

def setupOutput():
    RATE = 44100
    CHUNK = 128
    WIDTH = 2
    CHANNELS = 1

    gen = NoteGenerator(CHANNELS, RATE)
    p = pyaudio.PyAudio()

    def grabMore(in_data, frame_count, time_info, status):
        data = gen.generate(frame_count)
        return (data, pyaudio.paContinue)

    stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK,
                stream_callback=grabMore)

    stream.start_stream()
    return gen, (stream, p)

def finishOutput((stream, p)):
    stream.stop_stream()
    stream.close()

    p.terminate()
    return

def main():
    if len(sys.argv) > 1:
        wav_file = sys.argv[1]
    else:
        wav_file = None

    usb_dev = setupUSB()
    gen, pya = setupOutput()

    while True:
        try:
            seq = usb_dev.read(4)
            handleInput(gen, seq)
        except KeyboardInterrupt:
            print
            break
        except usb.core.USBError:
            pass

    finishOutput(pya)
    if wav_file is not None:
        gen.writeToFile(wav_file)
    return

if __name__ == "__main__":
    main()
