import numpy as np
from util import get_tube_file_name, window_size, tube_run_count, first_peak_n, tube_lengths, iris_count, effective_iris_count
from fit_util import moving_avg
from peak_detector import find_peaks


class TubeData:
    tube_run_count = tube_run_count
    first_peak_n = first_peak_n
    hz_per_volt = 1000
    avg_voltage_offset = 2.04
    delta_hz_per_volt = 30
    avg_length = 10

    def __init__(self, tube_run_index: int):
        data = np.loadtxt(get_tube_file_name(tube_run_index, include_path_prefix=True), delimiter=",", skiprows=2)
        frequency = data[:, 1]  # Initially in volts
        amplitude = data[:, 2]

        reordering = np.argsort(frequency)
        frequency = frequency[reordering]
        amplitude = amplitude[reordering]

        frequency += self.avg_voltage_offset
        frequency *= self.hz_per_volt

        # Handle flat start
        filter = (amplitude > 0.1) | (frequency > 500)
        frequency = frequency[filter]
        amplitude = amplitude[filter]

        self._frequency = frequency
        self._amplitude = amplitude

        self._amplitude_ma = moving_avg(amplitude, self.avg_length)
        self._amplitude_ma = self._amplitude_ma[self.avg_length - 1:]
        self._ma_frequency = frequency[(self.avg_length - 1) * 2:]
        self._peak_indices = find_peaks(self._amplitude_ma, self._ma_frequency, window_size[tube_run_index])
        self._first_peak_n = self.first_peak_n[tube_run_index]
        self._tube_length = tube_lengths[tube_run_index]
        self._iris_count = iris_count[tube_run_index]
        self._effective_iris_count = effective_iris_count[tube_run_index]

    @property
    def frequency(self):
        return self._frequency

    @property
    def amplitude(self):
        return self._amplitude

    @property
    def ma_frequency(self):
        return self._ma_frequency

    @property
    def amplitude_ma(self):
        return self._amplitude_ma

    @property
    def peak_frequencies(self):
        return self._ma_frequency[self._peak_indices]

    @property
    def peak_amplitudes(self):
        return self._amplitude_ma[self._peak_indices]

    @property
    def resonance_n(self):
        diff = np.diff(self.peak_frequencies)
        mean_diff = np.mean(diff[diff < 1.4 * np.mean(diff)])
        if self._iris_count > 0:
            mean_diff = np.mean(diff[diff > 0.5 * np.mean(diff)])
        n_delta = np.round(diff / mean_diff)
        n = np.zeros(len(n_delta) + 1)
        n[0] = self._first_peak_n
        n[1:] = n_delta
        return np.cumsum(n)

    @property
    def tube_length(self):
        return self._tube_length

    @property
    def iris_count(self):
        return self._iris_count

    @property
    def wavenumber(self):
        iris_count = self._effective_iris_count or 1
        wavelength_per_l = (iris_count - 1) * 1/2 + 1/2
        return 2 * np.pi * self.resonance_n * wavelength_per_l / (self.tube_length / 100)

    @property
    def angular_frequency(self):
        return 2 * np.pi * self.peak_frequencies

    @property
    def angular_frequency_delta(self):
        f_delta = self.peak_frequencies / self.hz_per_volt * self.delta_hz_per_volt
        return 2 * np.pi * f_delta
