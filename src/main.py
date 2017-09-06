import math
import astropy.constants
import numpy as np
import matplotlib.pyplot as plt
from celestialbody import CelestialBody
from radialvelocity import radial_velocity

PI = math.pi
AU = astropy.constants.au.value
M_JUP = astropy.constants.M_jup.value
M_SUN = astropy.constants.M_sun.value
# the number of days to run the test for
DURATION = 10

# Values for 51 Peg b as a test
mass_a = 0.472 * M_JUP
a = 0.0527 * AU
e = 0.013
i = 80 * PI/180
w = 58 * PI/180
# longitude of ascending node and true anomaly aren't that important here
z = 0
f = 0
t0 = 2450001
mass_b = 1.06 * M_SUN

body_a = CelestialBody(mass_a, a, e, i, z, w, f, t0)
body_b = CelestialBody(mass_b, 0, 0, 0, 0, 0, 0, 0)
(times,rv) = radial_velocity(body_a, body_b, t0, DURATION)
rv = np.divide(rv,1000)
plt.plot(times,rv)
plt.title('The RV Curve for 51 Peg b')
plt.xlabel('Time (JD)')
plt.ylabel('Velocity (km/s)')
plt.show()