import numpy as np


class SphericalResonator:
    angular_sweep_file = "data/output/spherical_angular_sweep_4970_Hz.csv"
    angular_sweep_frequency = 4970  # Hz
    degrees_per_second = 1

    def __init__(self):
        data = np.loadtxt(self.angular_sweep_file, delimiter=',', skiprows=2)
        self._angular_position = data[:, 0]
        self._amplitude = data[:, 2]

    @property
    def angular_position(self):
        return self._angular_position

    @property
    def amplitude(self):
        return self._amplitude


