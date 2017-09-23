'''
Function where, given the CelestialBody classes of two bodies (hence, their 
orbital elements and masses), a starting time, and a duration, calculates the 
RV curve starting at the given time and lasting the duration. 
'''
import math
import astropy.constants
import numpy as np
from celestialbody import CelestialBody

PI = math.pi
G = astropy.constants.G.value
AU = astropy.constants.au.value
DAY = 86400
# amount of points to calculate for the duration
_BIN_COUNT = 1000
# number of iterations to run Newton-Raphson to calculate eccentric anomaly
_ITERATIONS = 100

def _orbital_period(body_a, body_b):
    mass_a = body_a.get_mass()
    mass_b = body_b.get_mass()
    a = body_a.get_semimajor_axis()
    return math.sqrt(4*PI**2 / (G*(mass_a+mass_b)) * a**3) / DAY

def _mean_anomaly(body_a, body_b, t_i, t_f):
    T = _orbital_period(body_a, body_b)
    times = np.array([t_i])
    for i in range(1, int(_BIN_COUNT*(t_f-t_i))):
        times = np.append(times, [t_i + (i/_BIN_COUNT)])
    t0 = body_a.get_time_periapse()
    return times, 2*PI/T*np.subtract(times, t0)

def _eccentric_anomaly(e, M):
    E = M
    for i in range(0, _ITERATIONS):
        E = E - np.divide(E - e*np.sin(E) - M, np.subtract(1, e*np.cos(E)))
    return E

def _true_anomaly(body_a, body_b, t_i, t_f):
    times, M = _mean_anomaly(body_a, body_b, t_i, t_f)
    e = body_a.get_eccentricity()
    E = _eccentric_anomaly(e, M)
    return times, 2 * np.arctan(math.sqrt((1+e)/(1-e)) * np.tan(E/2))

# calculates RV by first calculating M(t), using that to find E, then f(E), 
# and ultimately v(f(E)) (aka changing the function from v(f) to v(t))
# returns the RV of body_a with respect to body_b
def radial_velocity(body_a, body_b, t_i, t_f):
    mass_a = body_a.get_mass()
    mass_b = body_b.get_mass()
    a = body_a.get_semimajor_axis()
    e = body_a.get_eccentricity()
    i = body_a.get_inclination()
    w = body_a.get_arg_periapse()
    times, f = _true_anomaly(body_a, body_b, t_i, t_f)
    return times, math.sqrt(G / ((mass_a+mass_b)*a*(1-e**2))) * \
        mass_b*math.sin(i) * np.add(np.cos(np.add(w,f)), e*math.cos(w))