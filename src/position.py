import math
import numpy as np
import astropy.constants
from radialvelocity import _true_anomaly
from celestialbody import CelestialBody

PI = math.pi
AU = astropy.constants.au.value

# returns the projected coordinates of the orbit wrt the star
def _coordinates(r, z, w, f, i):
    X = r * (math.cos(z) * np.cos(np.add(w, f)) - 
        math.sin(z) * np.sin(np.add(w, f)) * math.cos(i)) / AU
    Y = r * (math.sin(z) * np.cos(np.add(w, f)) + 
        math.cos(z) * np.sin(np.add(w, f)) * math.cos(i)) / AU
    return X, Y

# returns the radius of the orbit at true anomaly f
def _radius(body_a, f):
    a = body_a.get_semimajor_axis()
    e = body_a.get_eccentricity()
    return np.divide(a * (1 - e**2), np.add(1, e * np.cos(f)))

# returns the projected separation of body_a in AU with respect to body_b
def projected_separation(body_a, body_b, t_i, t_f):
    times, f = _true_anomaly(body_a, body_b, t_i, t_f)
    r = _radius(body_a, f)
    z = body_a.get_long_ascend_node()
    w = body_a.get_arg_periapse()
    i = body_a.get_inclination()
    X, Y = _coordinates(r, z, w, f, i)
    return times, np.sqrt(np.add(np.square(X), np.square(Y)))

# returns the projected separations in AU with respect to the center of mass
# we move the origin from the star to the CoM. since the star was originally 
# at the CoM, it should be x_com away from the CoM. naturally, the distance 
# from the planet to the CoM should be (dist - x_com)
def projected_separation_com(body_a, body_b, t_i, t_f):
    times, dist = projected_separation(body_a, body_b, t_i, t_f)
    mass_a = body_a.get_mass()
    mass_b = body_b.get_mass()
    x_com = (dist * mass_a) / (mass_a + mass_b)
    return times, dist - x_com, x_com

# returns the position angle of body_a in degrees with respect to body_b
def position_angle(body_a, body_b, t_i, t_f):
    times, f = _true_anomaly(body_a, body_b, t_i, t_f)
    r = _radius(body_a, f)
    z = body_a.get_long_ascend_node()
    w = body_a.get_arg_periapse()
    i = body_a.get_inclination()
    X, Y = _coordinates(r, z, w, f, i)
    return times, np.arctan2(Y, X) * 180 / PI

# returns the position angles in degrees with respect to the center of mass
# the star should always be opposite the planet with respect to the CoM. thus 
# its position angle should be 180 + (the planet's position angle), mod 360
def position_angle_com(body_a, body_b, t_i, t_f):
    times, plan_pa = position_angle(body_a, body_b, t_i, t_f)
    star_pa = (plan_pa + 180) % 360
    return times, plan_pa, star_pa
