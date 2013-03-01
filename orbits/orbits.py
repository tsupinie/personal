
from math import sqrt, sin, asin, cos, acos, tan, atan2, atan, radians, degrees, pi

import matplotlib
matplotlib.use('agg')
import pylab
from matplotlib.patches import Ellipse

_gravitational_const = 6.67383480e-11

_sun_mass = 1.756567e28

_kerbin_mass = 5.2915793e22
_kerbin_orbit_radius = 1.3599840256e10

_duna_mass = 4.5154812e21
_duna_orbit_radius = 2.0726155264e10

def _rotateVector(x_vec, y_vec, angle):
    len_vec = sqrt(x_vec ** 2 + y_vec ** 2)
    init_angle = atan2(y_vec, x_vec)

    rot_x_vec = len_vec * cos(angle + init_angle)
    rot_y_vec = len_vec * sin(angle + init_angle)
    return rot_x_vec, rot_y_vec

def circularVelocity(center_mass, radius):
    return sqrt(_gravitational_const * center_mass / radius)

def plotTransferEllipse(focus_x, focus_y, smaj_axis, true_anomaly1, true_anomaly2, file_name):
    pylab.figure(figsize=(8, 8))

    pylab.plot([ _kerbin_orbit_radius ], [ 0 ], 'bo')
    pylab.plot([ 0 ], [ _duna_orbit_radius ], 'ro')
    pylab.plot([ 0 ], [ 0 ], 'ko')

    pylab.plot([ focus_x ], [ focus_y ], 'kx')

    center_x = focus_x / 2
    center_y = focus_y / 2
    center_dist = sqrt(center_x ** 2 + center_y ** 2)
    smin_axis = sqrt(smaj_axis ** 2 - center_dist ** 2)
    cant_angle = degrees(atan2(-center_y, -center_x))

    eccentricity = center_dist / smaj_axis
    rad_true_anomaly1 = smaj_axis * (1 - eccentricity ** 2) / (1 + eccentricity * cos(true_anomaly1))
    rad_true_anomaly2 = smaj_axis * (1 - eccentricity ** 2) / (1 + eccentricity * cos(true_anomaly2))

    x_src, y_src = _rotateVector(rad_true_anomaly1, 0, true_anomaly1 + radians(cant_angle))
    x_dest, y_dest = _rotateVector(rad_true_anomaly2, 0, true_anomaly2 + radians(cant_angle))

    pylab.gca().add_patch(Ellipse([center_x, center_y], 2 * smaj_axis, 2 * smin_axis, angle=cant_angle, fc='none'))    

    pylab.gca().add_patch(Ellipse([0, 0], 2 * _duna_orbit_radius, 2 * _duna_orbit_radius, fc='none'))
    pylab.gca().add_patch(Ellipse([0, 0], 2 * _kerbin_orbit_radius, 2 * _kerbin_orbit_radius, fc='none'))

    pylab.plot([0, x_src], [0, y_src], 'k-')
    pylab.plot([0, x_dest], [0, y_dest], 'k-')

    pylab.xlim([-_duna_orbit_radius, _duna_orbit_radius])
    pylab.ylim([-_duna_orbit_radius, _duna_orbit_radius])

    pylab.savefig(file_name)
    pylab.close()
    return

def computeTransferEllipse(radius1, radius2, phase_angle):
    """
    Solve Lambert's Problem (http://en.wikipedia.org/wiki/Lambert%27s_problem)
    Essentially, given two planets, we can define a hyperbola with the two planets as the foci.  The foci
        for the transfer orbit must lie on the hyperbola.  We already know where one focus for the transfer
        orbit is: it's the sun.  This allows us to develop an equation for the hyperbola that constrains the
        locations of the transfer orbit foci.  We still need to pick a location for the other focus of the
        transfer orbit.  Currently, it's set to be the same y value in hyperbola coordinates as the sun.
    """

    # Find the parameters for the hyperbola
    point_distance = sqrt(radius1 ** 2 + radius2 ** 2 + 2 * radius1 * radius2 * cos(radians(phase_angle))) / 2.
    smaj_axis_hyperb = (radius2 - radius1) / 2
    smin_axis_hyperb = sqrt(point_distance ** 2 - smaj_axis_hyperb ** 2)
    eccentricity_hyperb = point_distance / smaj_axis_hyperb

    radius_mean = (radius1 + radius2) / 2

    # Find the location of the sun in hyperbola coordinates
    x_coord_sun = -radius_mean / eccentricity_hyperb
    y_coord_sun = smin_axis_hyperb * sqrt((x_coord_sun / smaj_axis_hyperb) ** 2 - 1)

    # Find the location of the other focus in hyperbola coordinates
    y_other_focus = y_coord_sun # Assumption for now.  I'll try to relax this later
    x_other_focus = smaj_axis_hyperb * sqrt(1 + (y_other_focus / smin_axis_hyperb) ** 2)
   
    smaj_axis_ell = (radius_mean + eccentricity_hyperb * x_other_focus) / 2
    # Find the true anomaly of the intial point on the transfer ellipse
    focus_vec_x = x_other_focus - x_coord_sun
    focus_vec_y = y_other_focus - y_coord_sun
    len_focus_vec = sqrt(focus_vec_x ** 2 + focus_vec_y ** 2)

    rot_angle = pi - asin(radius2 / (2 * point_distance) * sin(radians(phase_angle)))
    focus_ss_coords_x, focus_ss_coords_y = _rotateVector(focus_vec_x, focus_vec_y, rot_angle) 

    x_dest, y_dest = _rotateVector(radius2, 0, radians(phase_angle))
    true_anomaly1 = acos(-(focus_ss_coords_x * radius1 + focus_ss_coords_y * 0) / (radius1 * len_focus_vec))
    true_anomaly2 = acos(-(focus_ss_coords_x * x_dest + focus_ss_coords_y * y_dest) / (radius2 * len_focus_vec))

    return focus_ss_coords_x, focus_ss_coords_y, smaj_axis_ell, true_anomaly1, true_anomaly2

def computeTransferTime(true_anomaly1, true_anomaly2, smaj_axis, eccentricity):
    def computeTrueAnomalyIntegral(true_anomaly):
        term1 = eccentricity * sin(true_anomaly) / ((eccentricity ** 2 - 1) * (eccentricity * cos(true_anomaly) + 1))
        term2 = 2 * atan((1 - eccentricity) * tan(true_anomaly / 2) / sqrt(1 - eccentricity ** 2)) / (1 - eccentricity ** 2) ** 1.5
        return term1 - term2

    print computeTrueAnomalyIntegral(true_anomaly1)
    print computeTrueAnomalyIntegral(true_anomaly2)

    return (computeTrueAnomalyIntegral(true_anomaly2) - computeTrueAnomalyIntegral(true_anomaly1)) * sqrt(smaj_axis ** 3 * (1 - eccentricity ** 2) ** 3 / (_gravitational_const * _sun_mass))

def computeSingleTransfer(radius1, radius2, phase_angle):
    return

def computeDoubleTransfer():
    return

def main():
    transfer_focus_x, transfer_focus_y, transfer_smaj, true_anomaly1, true_anomaly2  = computeTransferEllipse(_kerbin_orbit_radius, _duna_orbit_radius, 90.)
    transfer_eccentricity = sqrt((transfer_focus_x / 2) ** 2 + (transfer_focus_y / 2) ** 2) / transfer_smaj

    print computeTransferTime(true_anomaly1, true_anomaly2, transfer_smaj, transfer_eccentricity)

    plotTransferEllipse(transfer_focus_x, transfer_focus_y, transfer_smaj, true_anomaly1, true_anomaly2, "transfer.png")
    return

if __name__ == "__main__":
    main()
