import math
import numpy as np
import astropy.constants
from matplotlib import pyplot as plt, rc 
from celestialbody import CelestialBody
from radialvelocity import radial_velocity
from position import projected_separation, position_angle
rc('text', usetex = True)

PI = math.pi
AU = astropy.constants.au.value
M_JUP = astropy.constants.M_jup.value
M_SUN = astropy.constants.M_sun.value
# the number of days to run the test for
DURATION = 10

# TEST DATA
# values for 51 Peg b
mass_a = 0.472 * M_JUP
a = 0.0527 * AU
e = 0.013
i = 80 * PI / 180
z = 0
w = 58 * PI / 180
f = 0
t0 = 2450001
# values for 51 Peg
mass_b = 1.06 * M_SUN
body_a = CelestialBody(mass_a, a, e, i, z, w, f, t0)
body_b = CelestialBody(mass_b, a, e, i, z, (w + PI) % (2 * PI), f, t0)

# TEST FOR RV CORRECTNESS
'''
(times_p, rv_p) = radial_velocity(body_a, body_b, t0, DURATION)
(times_s, rv_s) = radial_velocity(body_b, body_a, t0, DURATION)
rv_p = np.divide(rv_p, 1000)
plt.figure(1)
plt.subplot(211)
plt.plot(times_p, rv_p)
plt.title(r'\textbf{The RV Curve for 51 Peg b}')
plt.xlabel('Time (JD)')
plt.ylabel('Velocity (km/s)')
plt.ticklabel_format(useOffset=False, scientific=False)
plt.subplot(212)
plt.plot(times_s, rv_s)
plt.title(r'\textbf{The RV Curve for 51 Peg}')
plt.xlabel('Time (JD)')
plt.ylabel('Velocity (m/s)')
plt.ticklabel_format(useOffset=False, scientific=False)
plt.tight_layout()
plt.show()
'''

# TEST FOR PROJECTED SEPARATION AND POSITION ANGLE CORRECTNESS
Y, Z = projected_separation(body_a, body_b, t0)
vals = np.sqrt(np.square(Y) + np.square(Z))
print(vals)
print(position_angle(body_a, body_b, t0))