import math
import numpy as np
from astropy import constants, time
from matplotlib import pyplot as plt, rc 
from celestialbody import CelestialBody
from radialvelocity import radial_velocity
from position import projected_separation, position_angle
from transit import transit
from astrometry import (astrometry_planet, astrometry_parallax, 
    astrometry_proper)

PI = math.pi
AU = constants.au.value
M_JUP = constants.M_jup.value
M_SUN = constants.M_sun.value
R_EARTH = constants.R_earth.value
R_SUN = constants.R_sun.value
# the start and end times to run the "detections" for
START = (time.Time('2017-08-01 00:00:00', format='iso', scale='utc')).jd
END = (time.Time('2018-01-01 00:00:00', format='iso', scale='utc')).jd

# values for HD 80606 b
# mass (kg)
mass_a = 3.94 * M_JUP
# radius (m)
r_a = 10.98 * R_EARTH
# semimajor aixs (m)
a = 0.449 * AU
# eccentricity
e = 0.9332
# inclination (rad)
i = 89.32 * PI / 180
# longitude of ascending node (rad)
z = PI
# argument of periapse (rad)
w = 300.80 * PI / 180
# true anomaly
f = 0
# time of periapse (JD)
t0 = 2454424.852
# values for HD 80606
# mass (kg)
mass_b = 0.97 * M_SUN
# radius (m)
r_b = 0.978 * R_SUN
# HD 80606 b
body_a = CelestialBody(mass_a, r_a, a, e, i, z, w, f, t0)
# HD 80606
body_b = CelestialBody(mass_b, r_b, a, e, i, z, (w + PI) % (2 * PI), f, t0)

# Question 2
#'''
times, rv = radial_velocity(body_b, body_a, START, END)
rv_max = max(rv)
rv_min = min(rv)
# get the times the max and min of RV will be
max_idx = np.argpartition(rv, -2)[-2:]
min_idx = np.argpartition(rv, 2)[:2]
print("Time(s) of RV max:", times[max_idx])
print("Time(s) of RV min:", times[min_idx])
# plot the stellar RV curve
plt.figure(1)
plt.plot(times - 2450000, rv)
plt.xlabel('Time (JD - 2450000)')
plt.ylabel('Radial Velocity (m/s)')
plt.ticklabel_format(useOffset=False, scientific=False)
plt.tight_layout()
plt.show()
plt.close()
#'''

# Question 3
#'''
times, transits = transit(body_a, body_b, START, END)
# get the times body_a is transiting body_b, if at all
print('Times of transit:')
for idx, time in enumerate(times):
    if transits[idx] == 1:
        print(time)
# plot the occurrences of transits
plt.figure(2)
plt.plot(times - 2450000, transits)
plt.xlabel('Time (JD - 2450000)')
plt.ylabel('Transit Occurrence')
plt.ticklabel_format(useOffset=False, scientific=False)
plt.tight_layout()
plt.show()
plt.close()
#'''

# Question 4
#'''
# HD 80606 has a magnitude of 8.93, so average precisions for 8.32 and 9.73
# astrometric uncertainty of GAIA for position, parallax, proper motion (mas)
u_pos = 0.36
u_par = 0.68
u_prop = 0.105
# equatorial coordinates of HD 80606 (degrees)
ra = (9 + 22/60 + 35.2/3600) * 180/12
dec = 50 + 36/60 + 29/3600
# distance to HD 80606 from Earth (pc)
dist = 58.4
# proper motion of HD 80606 (mas/yr)
m_ra = 45.76
m_dec = 16.56
# array of 100 randomly timed epochs over 5 years beginning with START
times = np.sort(np.random.rand(100)) * 365 * 5 + START
# RA vs t, DEC vs t, DEC vs RA for planet
ra_plan, dec_plan = astrometry_planet(ra, dec, dist, body_a, body_b, times)
plt.figure(3)
plt.xlabel('Time (JD - 2450000)')
plt.ylabel('Change in Right Ascension (mas)')
plt.errorbar(times - 2450000, ra_plan, xerr=u_pos, yerr=u_pos, ecolor='g')
plt.ticklabel_format(useOffset=False, scientific=False)
plt.tight_layout()
plt.figure(4)
plt.xlabel('Time (JD - 2450000)')
plt.ylabel('Change in Declination (mas)')
plt.errorbar(times - 2450000, dec_plan, xerr=u_pos, yerr=u_pos, ecolor='g')
plt.ticklabel_format(useOffset=False, scientific=False)
plt.tight_layout()
plt.figure(5)
plt.xlabel('Change in Right Ascension (mas)')
plt.ylabel('Change in Declination (mas)')
plt.errorbar(ra_plan, dec_plan, xerr=u_pos, yerr=u_pos, ecolor='g')
plt.ticklabel_format(useOffset=False, scientific=False)
plt.tight_layout()
plt.show()
# RA vs t, DEC vs t, DEC vs RA for planet + parallax
ra_par, dec_par = astrometry_parallax(ra, dec, dist, body_a, body_b, times)
plt.figure(6)
plt.xlabel('Time (JD - 2450000)')
plt.ylabel('Change in Right Ascension (mas)')
plt.errorbar(times - 2450000, ra_par, xerr=u_par, yerr=u_par, ecolor='g')
plt.ticklabel_format(useOffset=False, scientific=False)
plt.tight_layout()
plt.figure(7)
plt.xlabel('Time (JD - 2450000)')
plt.ylabel('Change in Declination (mas)')
plt.errorbar(times - 2450000, dec_par, xerr=u_par, yerr=u_par, ecolor='g')
plt.ticklabel_format(useOffset=False, scientific=False)
plt.tight_layout()
plt.figure(8)
plt.xlabel('Change in Right Ascension (mas)')
plt.ylabel('Change in Declination (mas)')
plt.errorbar(ra_par, dec_par, xerr=u_par, yerr=u_par, ecolor='g')
plt.ticklabel_format(useOffset=False, scientific=False)
plt.tight_layout()
plt.show()
# RA vs t, DEC vs t, DEC vs RA for planet + parallax + proper motion
ra_prop, dec_prop = astrometry_proper(m_ra, m_dec, ra, dec, dist, body_a, 
    body_b, times)
plt.figure(9)
plt.xlabel('Time (JD - 2450000)')
plt.ylabel('Change in Right Ascension (mas)')
plt.errorbar(times - 2450000, ra_prop, xerr=u_prop, yerr=u_prop, ecolor='g')
plt.ticklabel_format(useOffset=False, scientific=False)
plt.tight_layout()
plt.figure(10)
plt.xlabel('Time (JD - 2450000)')
plt.ylabel('Change in Declination (mas)')
plt.errorbar(times - 2450000, dec_prop, xerr=u_prop, yerr=u_prop, ecolor='g')
plt.ticklabel_format(useOffset=False, scientific=False)
plt.tight_layout()
plt.figure(11)
plt.xlabel('Change in Right Ascension (mas)')
plt.ylabel('Change in Declination (mas)')
plt.errorbar(ra_prop, dec_prop, xerr=u_prop, yerr=u_prop, ecolor='g')
plt.ticklabel_format(useOffset=False, scientific=False)
plt.tight_layout()
plt.show()
plt.close()
#'''