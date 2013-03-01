
import numpy as np
import matplotlib
matplotlib.use('agg')
import pylab

def plotDensityTimeseries(time, temp, pres, name):
    density = pres / (287. * temp)
#   rm_density = (density[:-2] + density[1:-1] + density[2:]) / 3
#   density[1:-1] = rm_density
    drhodt = np.gradient(density, 300.)

    pylab.clf()
    pylab.plot(time, drhodt)
    pylab.plot([time[0], time[-1]], [0, 0], 'k--')
    pylab.xlim(time[0], time[-1])
    pylab.ylim(-1.5e-5, 1.5e-5)

    pylab.xticks(time[::12])
    pylab.savefig("drhodt_%s.png" % name)

    pylab.clf()
    pylab.plot(time, density)
    pylab.xlim(time[0], time[-1])
    pylab.ylim(1.09, 1.17)

    pylab.xticks(time[::12])
    pylab.savefig("density_%s.png" % name)

    argmin_drhodt = np.argmin(drhodt)
    print -(1 / density[argmin_drhodt] * drhodt[argmin_drhodt] + -1.5e-4) * 1000
    return

def getMTSData(file_name):
    mts = np.loadtxt(file_name, usecols=(2, 4, 12), skiprows=3)
    
    time = mts[:, 0] / 60.
    temp = mts[:, 1] + 273.15
    pres = mts[:, 2] * 100
   
    return time, temp, pres

def main():
    time, temp, pres = getMTSData("20080501wash.mts")
    plotDensityTimeseries(time, temp, pres, "wash")

    time, temp, pres = getMTSData("20110518nrmn.mts")
    plotDensityTimeseries(time, temp, pres, "nrmn")
    return

if __name__ == "__main__":
    main()
