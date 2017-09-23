import math
import astropy.constants
import numpy as np
from celestialbody import CelestialBody
from radialvelocity import _true_anomaly
from position import projected_separation

AU = astropy.constants.au.value

# returns when body_a transits body_b, if at all
def transit(body_a, body_b, t_i, t_f):
    # used for checking if planet is in front of the star
    f = _true_anomaly(body_a, body_b, t_i, t_f)[1]
    w = body_a.get_arg_periapse()
    times, dists = projected_separation(body_a, body_b, t_i, t_f)
    dists = (np.multiply(dists, AU)).tolist()
    r_star = body_b.get_radius()
    transits = []
    # transits when its projected separation is less than r_star and 
    # the planet is in front of the star
    for i, dist in enumerate(dists):
        if dist < r_star and math.sin(w + f[i]) > 0:
            transits.append(1)
        else:
            transits.append(0)
    return times, transits