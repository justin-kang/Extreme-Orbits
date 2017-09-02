'''
Class representing celestial objects, such as planets or stars. Contains 
information about the orbital information about said objects, which is 
obtained from construction or setters with user input.
'''
class CelestialBody:
    _semimajor_axis = None
    _inclination = None
    # longitude of ascending node
    _long_ascend_node = None
    # argument of periapse
    _arg_periapse = None
    # time of periapse passage
    _time_periapse = None
    _true_anomoly = None

    def __init__(self, smaxis, inclin, longnode, arg, time, anom):
        self.set_semimajor_axis(smaxis)
        self.set_inclination(inclin)
        self.set_long_ascend_node(longnode)
        self.set_arg_periapse(arg)
        self.set_time_periapse(time)
        self.set_true_anomoly(anom)

    @staticmethod
    def _check_num(num):
        try:
            float(num)
            return True
        except (TypeError, ValueError):
            return False

    def set_semimajor_axis(self):
        while not _check_num(self._semimajor_axis):
            self._semimajor_axis = input('Enter semimajor axis: ')

    def set_inclination(self):
        while not _check_num(self._inclination):
            self._inclination = input('Enter inclination: ')

    def set_long_ascend_node(self):
        while not _check_num(self._long_ascend_node):
            self._long_ascend_node = input(
                'Enter the longitude of ascending node: ')

    def set_arg_periapse(self):
        while not _check_num(self._arg_periapse):
            self._arg_periapse = input('Enter the argument of periapse: ')

    def set_time_periapse(self):
        while not _check_num(self._time_periapse):
            self._time_periapse = input(
                'Enter the time of periapse passage: ')

    def set_true_anomoly(self):
        while not _check_num(self._true_anomoly):
            self._true_anomoly = input('Enter the true anomoly: ')

    def get_semimajor_axis(self):
        return self._semimajor_axis

    def get_inclination(self):
        return self._inclination

    def get_long_ascend_node(self):
        return self._long_ascend_node

    def get_arg_periapse(self):
        return self._arg_periapse

    def get_time_periapse(self):
        return self._time_periapse

    def get_true_anomoly(self):
        return self._true_anomoly
