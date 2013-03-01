
import matplotlib
matplotlib.use('agg')
import pylab

import soundinglib
import parselib

def main():
    sounding = parselib.parse(open("/Users/tsupinie/Documents/20130129_00Z_KOUN_snd.txt", 'r'), 'SPC')

    pylab.figure(figsize=(8, 10))
    pylab.axes((0.05, 0.05, 0.9, 0.9))

    soundinglib.plotSkewTBackground(pylab.gca())
    soundinglib.plotProfile(sounding['temperature'], sounding['pressure'], color='r', lw=1.5)
    soundinglib.plotProfile(sounding['dewpoint'], sounding['pressure'], color='g', lw=1.5)
    soundinglib.plotWinds(sounding['u_wind'], sounding['v_wind'], sounding['pressure'])

    trace_temp, trace_pres = soundinglib.computeParcelTrace(sounding['temperature'][1], sounding['dewpoint'][1], sounding['pressure'][1:])
    soundinglib.plotProfile(trace_temp, trace_pres, color='#660000', lw=2.5, linestyle='--')

    pylab.savefig("20130129_KOUN.png")
    return

if __name__ == "__main__":
    main()
