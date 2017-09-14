'''
Class representing celestial objects, such as planets or stars. Contains 
information about the mass and orbital information about said objects, which 
is obtained from explicit values during construction or user input.
'''
from math import pi
import astropy.constants

M_SUN = astropy.constants.M_sun.value
M_JUP = astropy.constants.M_jup.value
M_EARTH = astropy.constants.M_earth.value
AU = astropy.constants.au.value

class CelestialBody:
    _mass = None
    _semimajor_axis = None
    _eccentricity = None
    _inclination = None
    # longitude of ascending node
    _long_ascend_node = None
    # argument of periapse
    _arg_periapse = None
    _true_anomaly = None    
    # time of periapse passage
    _time_periapse = None

    def __init__(self):
        self.set_mass(None)
        self.set_semimajor_axis(None)
        self.set_eccentricity(None)
        self.set_inclination(None)
        self.set_long_ascend_node(None)
        self.set_arg_periapse(None)
        self.set_true_anomaly(None)
        self.set_time_periapse(None)

    def __init__(self, m, a, e, i, z, w, f, t):
        self.set_mass(m)
        self.set_semimajor_axis(a)
        self.set_eccentricity(e)
        self.set_inclination(i)
        self.set_long_ascend_node(z)
        self.set_arg_periapse(w)
        self.set_true_anomaly(f)
        self.set_time_periapse(t)

    # requests user for unit and mass, stores as kilograms
    def set_mass(self, mass):
        if mass is None:
            while not _check_num(self._mass):
                unit = input('Enter unit of mass: ')
                mass = input('Enter mass: ')
                if unit == 'M_sun':
                    self._mass = float(mass) * M_SUN
                elif unit == 'M_jup':
                    self._mass = float(mass) * M_JUP
                elif unit == 'M_earth':
                    self._mass = float(mass) * M_EARTH
                else:
                    print('Invalid units, '
                        'use \'M_sun,\' \'M_jup,\' or \'M_earth\'')
        else:
            self._mass = mass

    def set_eccentricity(self, eccentricity):
        if eccentricity is None:
            while not _check_num(self._eccentricity):
                self._eccentricity = input('Enter eccentricity: ')
        else:
            self._eccentricity = eccentricity

    # stores as meters
    def set_semimajor_axis(self, semimajor_axis):
        if semimajor_axis is None:
            while not _check_num(self._semimajor_axis):
                dist = input('Enter semimajor axis (AU): ')
                self._semimajor_axis = float(dist) * AU
        else:
            self._semimajor_axis = semimajor_axis

    # stores as radians
    def set_inclination(self, inclination):
        if inclination is None:
            while not _check_num(self._inclination):
                inclination = input('Enter inclination (degrees): ')
                self._inclination = float(inclination) * pi / 180
        else:
            self._inclination = inclination

    # stores as radians
    def set_long_ascend_node(self, long_ascend_node):
        if long_ascend_node is None:
            while not _check_num(self._long_ascend_node):
                long_ascend_node = input(
                    'Enter the longitude of ascending node (degrees): ')
                self._long_ascend_node = float(long_ascend_node) * pi / 180
        else:
            self._long_ascend_node = long_ascend_node

    # stores as radians
    def set_arg_periapse(self, arg_periapse):
        if arg_periapse is None:
            while not _check_num(self._arg_periapse):
                arg_periapse = input(
                    'Enter the argument of periapse (degrees): ')
                self._arg_periapse = float(arg_periapse) * pi / 180
        else:
            self._arg_periapse = arg_periapse

    # stores as radians
    def set_true_anomaly(self, true_anomaly):
        if true_anomaly is None:
            while not _check_num(self._true_anomaly):
                true_anomaly = input('Enter the true anomaly (degrees): ')
                self._true_anomaly = float(true_anomaly) * pi / 180
        else:
            self._true_anomaly = true_anomaly

    def set_time_periapse(self, time_periapse):
        if time_periapse is None:
            while not _check_num(self._time_periapse):
                self._time_periapse = input(
                    'Enter the time of periapse passage (JD): ')
        else:
            self._time_periapse = time_periapse

    def get_mass(self):
        return self._mass

    def get_semimajor_axis(self):
        return self._semimajor_axis

    def get_eccentricity(self):
        return self._eccentricity

    def get_inclination(self):
        return self._inclination

    def get_long_ascend_node(self):
        return self._long_ascend_node

    def get_arg_periapse(self):
        return self._arg_periapse

    def get_true_anomaly(self):
        return self._true_anomaly

    def get_time_periapse(self):
        return self._time_periapse

# validates user input
def _check_num(num):
    try:
        float(num)
        return True
    except (TypeError, ValueError):
        return False