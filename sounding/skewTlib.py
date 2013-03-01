
import numpy as np
from scipy.integrate import odeint

import matplotlib
#matplotlib.use('agg')
#import pylab
import matplotlib.transforms as transforms
from matplotlib.scale import LogScale

import cPickle

_stlp_data_transform, _stlp_xlabel_transform, _stlp_ylabel_transform = 0, 0, 0
_figure, _axes = 0, 0

_p_min = 100
_p_max = 1050
_p_step = 100

_T_plot_min = -110
_T_min = -30
_T_max = 50
_T_step = 10
 
_th_min = -30
_th_max = 200
_th_step = 10   

_the_min = -20
_the_max = 50
_the_step = 5

def _buildTransform():
    global _stlp_data_transform, _stlp_xlabel_transform, _stlp_ylabel_transform

    data_figure_trans = _axes.transData + _figure.transFigure.inverted()

    identity_matrix = np.zeros((3, 3))
    for idx in range(3): identity_matrix[idx, idx] = 1

    # Create the affine matrix for the skew transform.  This only works in data coordinates.  We'll fix that later ...
    skew_matrix = np.copy(identity_matrix)
    skew_matrix[0, 1] = np.tan(45 * np.pi / 180)
    skew_transform = transforms.Affine2D(skew_matrix)

    # Create the logarithmic transform in the y.
    log_p_transform = transforms.blended_transform_factory(transforms.Affine2D(), LogScale(_axes.yaxis, basey=10).get_transform())

    # The log transform shrinks everything to log(p) space, so define a scale factor to blow it back up to a reasonable size.
    p_bnd_trans = log_p_transform.transform(np.array([[0, _p_min], [0, _p_max]]))[:, 1]
    scale_factor = (_p_max - _p_min) / (p_bnd_trans[1] - p_bnd_trans[0])

    # Define the affine transform for the flip and another for the scale back to reasonable coordinates after the log transform.
    flip_transform = transforms.Affine2D.identity().scale(1, -1)
    preskew_scale_transform = transforms.Affine2D().translate(0, p_bnd_trans[1]).scale(1, scale_factor).translate(0, _p_min)
    postskew_move_transform = transforms.Affine2D().translate(0, _p_min)

    # Define a transform that basically does everything but the skew so we can figure out where the 1000 mb level is and skew around that line.
    prelim_data_transform = log_p_transform + flip_transform + preskew_scale_transform + data_figure_trans
    marker = prelim_data_transform.transform(np.array([[_T_min, 1000]]))[0, 1]

    # Add a translation to that marker point into the data-figure transform matrix.
    data_figure_trans += transforms.Affine2D().translate(0, -marker)

    # Define our skew transform in figure coordinates.
    figure_skew_transform = data_figure_trans + skew_transform + data_figure_trans.inverted()

    # Create our skew-T log-p transform matrix.  It does the log-p transform first, then the flip, then the scale, then the skew.
    _stlp_data_transform = log_p_transform + flip_transform + preskew_scale_transform + figure_skew_transform + _axes.transData

    # Create a blended transform where the y axis is the log-p, but the x axis is the axes transform (for adding pressure labels and wind barbs).
    _stlp_xlabel_transform = transforms.blended_transform_factory(_stlp_data_transform, _axes.transAxes)
    _stlp_ylabel_transform = transforms.blended_transform_factory(_axes.transAxes, _stlp_data_transform)
    return

def saturationVaporPressure(temperature):
    L = 2.5e6
    R_v = 461.5
    return 611 * np.exp(L / R_v * (1 / 273.15 - 1 / temperature))

def mixingRatio(vapor_pressure, pressure):
    epsilon = 0.622
    return (epsilon * vapor_pressure) / (pressure - vapor_pressure)

def moistAdiabaticLapseRate(temperature, pressure):
    R_d = 278.
    R_v = 461.5
    c_p = 1003.5
    L = 2.5e6

    sat_mix_rat = mixingRatio(saturationVaporPressure(temperature), pressure)
    moist_term1 = (sat_mix_rat * L) / (R_d * temperature) 
    moist_term2 = (sat_mix_rat * L ** 2) / (R_v * c_p * temperature ** 2)

    return ((1 + moist_term1) * temperature * R_d) / ((1 + moist_term2) * pressure * c_p)    

def pseudoadiabaticLapseRate(temperature, pressure):
    R_d = 278.
    epsilon = 0.622
    c_p = 1003.5
    L = 2.5e6

    sat_mix_rat = mixingRatio(saturationVaporPressure(temperature), pressure)
    moist_term1 = (sat_mix_rat * L) / (R_d * temperature) 
    moist_term2 = (sat_mix_rat * L ** 2 * (epsilon + sat_mix_rat)) / (R_d * c_p * temperature ** 2)
      
    return ((1 + sat_mix_rat) * (1 + moist_term1) * temperature * R_d) / ((1 + sat_mix_rat + moist_term2) * pressure * c_p)    

def plotSounding(mpl_figure, **kwargs):
    global _figure, _axes

    _figure = mpl_figure
    _figure.clf(keep_observers=True)

    _figure.delaxes(_figure.gca())
    _figure.set_dpi(100)

    _axes = matplotlib.axes.Axes(_figure, (0, 0, 1, 1)) 
    _axes.axes.get_xaxis().set_visible(False)
    _axes.axes.get_yaxis().set_visible(False)
    _figure.add_axes(_axes)

    _axes.set_xlim((_T_min, _T_max))
    _axes.set_ylim((_p_min, _p_max))

    if type(_stlp_data_transform) == int:
        _buildTransform()

    # Draw the isobars.
    for p_line in range(_p_min, _p_max + _p_step, _p_step):
        _axes.plot([_T_plot_min, _T_max], [p_line, p_line], color='k', lw=0.75, transform=_stlp_data_transform)
        _axes.text(0, p_line, "%d" % p_line, va='center', transform=_stlp_ylabel_transform)

    # Draw the isotherms.
    for T_line in range(_T_plot_min, _T_max + _T_step, _T_step):
        if T_line < 0:
            weight = 0.75
            color = 'c'
        elif T_line > 0: 
            color = '#880000'
            weight = 0.75
        else: 
            weight = 1
            color = 'b'

        _axes.plot([T_line, T_line], [_p_min, _p_max], color=color, lw=weight, transform=_stlp_data_transform)
        _axes.text(T_line, 1000, "%d" % T_line, ha='center', transform=_stlp_data_transform)

    # Draw the dry adiabats.
    for th_line in range(_th_min, _th_max + _th_step, _th_step):
        p_th = np.arange(_p_min, _p_max + 10., 10.)
        t_th = (th_line + 273.15) * (p_th / 1000.) ** (2. / 7.) - 273.15
        _axes.plot(t_th, p_th, color='#802a2a', lw=0.75, transform=_stlp_data_transform)

    # Draw the mixing ratio lines.
    for w_line in [ 1, 2, 3, 5, 8, 12, 16, 20 ]:
        p_w = np.arange(600., 1010., 10.)
        e_w = (p_w * 100 * w_line / 1000.) / (w_line / 1000. + 0.622)
        td_w = 1 / (1/273.0 - 461.5 / 2.5e6 * np.log(e_w / 611.)) - 273.15
        _axes.plot(td_w, p_w, color='#7fff00', lw=0.75, linestyle='--', transform=_stlp_data_transform)
        _axes.text(td_w[0], p_w[0], "%d" % w_line, color="#7fff00", ha='center', transform=_stlp_data_transform)

    # Draw the moist adiabats.
    for the_line in xrange(_the_min, _the_max + _the_step, _the_step):
        p_the_above = np.arange(_p_min, 1010., 10.)
        p_the_below = np.arange(1000., _p_max + 10., 10.)

        t_the_above = odeint(moistAdiabaticLapseRate, the_line + 273.15, 100 * p_the_above[::-1])[::-1,0] - 273.15
        t_the_below = odeint(moistAdiabaticLapseRate, the_line + 273.15, 100 * p_the_below)[:,0] - 273.15

        p_the = np.concatenate((p_the_above, p_the_below[1:]))
        t_the = np.concatenate((t_the_above, t_the_below[1:]))

        _axes.plot(t_the, p_the, color='#2e8b57', lw=0.75, linestyle=':', transform=_stlp_data_transform)

#   pylab.plot([0.95, 0.95], [p_min, p_max], color='k', lw=0.5, transform=stlp_ylabel_transform)

    p_snd = kwargs['p']

    if 'pt' in kwargs:
        t_snd = kwargs['pt'] * (p_snd / 1000.) ** (2. / 7.) - 273.15
    else:
        t_snd = kwargs['t']

    if 'qv' in kwargs:
        e_snd = (p_snd * kwargs['qv']) / (kwargs['qv'] + 0.622)
        td_snd = 1 / (1/273.0 - 461.5 / 2.5e6 * np.log(e_snd / 6.11)) - 273.15
    else:
        td_snd = kwargs['td']

    _axes.plot(t_snd, p_snd, lw=1.5, color='r', transform=_stlp_data_transform)
    _axes.plot(td_snd, p_snd, lw=1.5, color='g', transform=_stlp_data_transform)

#   t_barb_locs, p_barb_locs = np.swapaxes(stlp_ylabel_transform.transform(np.dstack((0.95 * np.ones(good_idxs.shape), p_obs_snd[good_idxs]))[0]), 0, 1)

#   print t_barb_locs
#   print p_barb_locs

#   pylab.barbs(t_barb_locs, p_barb_locs, u_obs_snd[good_idxs], v_obs_snd[good_idxs])

    _axes.set_xlim((_T_min, _T_max))
    _axes.set_ylim((_p_min, _p_max))

    _figure.canvas.draw()

#   pylab.savefig(file_name)
    return

def xyToTP(x, y, flip=False):
    if type(x) in [ int, float ]:
        x = [ x ]
    if type(y) in [ int, float ]:
        y = [ y ]

    points = np.array(zip(x, y))

    if flip:
        fig_points = _figure.transFigure.inverted().transform(points)
        fig_x, fig_y = zip(*fig_points)
        flip_fig_points = zip(fig_x, [ 1 - y for y in fig_y ])        
        points = _figure.transFigure.transform(flip_fig_points)

    return _stlp_data_transform.inverted().transform(points)

def tpToXY(T, p, flip=False):
    if not hasattr(T, '__iter__'):
        T = [ T ]
    if not hasattr(p, '__iter__'):
        p = [ p ]

    points = np.array(zip(T, p))

    trans_points = _stlp_data_transform.transform(points)

    if flip:
        fig_points = _figure.transFigure.inverted().transform(trans_points)
        fig_x, fig_y = zip(*fig_points)
        flip_fig_points = zip(fig_x, [ 1 - y for y in fig_y ])        
        trans_points = _figure.transFigure.transform(flip_fig_points)

    return trans_points
def main():
#   sounding = cPickle.load(open('proximity2.pkl', 'r'))
#   u_obs_snd = sounding['u_wind']
#   v_obs_snd = sounding['v_wind']
#   t_obs_snd = sounding['temperature']
#   td_obs_snd = sounding['dewpoint']
#   p_obs_snd = sounding['pressure']

#   good = (u_obs_snd != 9999.0) & (v_obs_snd != 9999.0) & (t_obs_snd != 999.0) & (td_obs_snd != 999.0) & (p_obs_snd != 9999.0)
#   good_idxs = np.where(good)[0]

    figure = pylab.figure(figsize=(6, 8))# matplotlib.figure.Figure(figsize=(6, 8))

    plotSounding(figure, p=[], t=[], td=[], u=[], v=[])

    figure.savefig("proximity2.png")
    return

if __name__ == "__main__":
    main()
