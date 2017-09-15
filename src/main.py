import math
import numpy as np
from astropy import constants, time
from matplotlib import pyplot as plt, rc 
from celestialbody import CelestialBody
from radialvelocity import radial_velocity
from position import projected_separation, position_angle
rc('text', usetex = True)

# constants
PI = math.pi
AU = constants.au.value
M_JUP = constants.M_jup.value
M_SUN = constants.M_sun.value
# the start and end times to run the "detections" for
START = (time.Time('2017-08-01 00:00:00', format='iso', scale='utc')).jd
END = (time.Time('2018-01-01 00:00:00', format='iso', scale='utc')).jd

# https://exoplanetarchive.ipac.caltech.edu/cgi-bin/DisplayOverview/nph-
# DisplayOverview?objname=HD+80606+b
# values for HD 80606 b
mass_a = 3.94 * M_JUP
a = 0.449 * AU
e = 0.9332
i = 89.32
z = 0
w = 300.80 * PI / 180
f = 0
t0 = 2454424.852
# values for HD 80606
mass_b = 0.97 * M_SUN
HD_80606_b = CelestialBody(mass_a, a, e, i, z, w, f, t0)
HD_80606 = CelestialBody(mass_b, a, e, i, z, (w + PI) % (2 * PI), f, t0)

# Question 2
times_p, rv_p = radial_velocity(HD_80606_b, HD_80606, START, END)
times_s, rv_s = radial_velocity(HD_80606, HD_80606_b, START, END)
rv_p = np.divide(rv_p, 1000)
plt.figure(1)
plt.subplot(211)
plt.plot(times_p, rv_p)
plt.title(r'\textbf{The RV Curve for HD 80606 b}')
plt.xlabel('Time (JD)')
plt.ylabel('Velocity (km/s)')
plt.ticklabel_format(useOffset=False, scientific=False)
plt.subplot(212)
plt.plot(times_s, rv_s)
plt.title(r'\textbf{The RV Curve for HD 80606}')
plt.xlabel('Time (JD)')
plt.ylabel('Velocity (m/s)')
plt.ticklabel_format(useOffset=False,  scientific=False)
plt.tight_layout()
plt.show()

# Question 3



# Question 4

