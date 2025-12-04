import math

from util import get_all_tube_file_names, path_prefix
import numpy as np


file_names = get_all_tube_file_names(include_iris=True, include_path_prefix=True)
voltage_freq_scale_minima = []

for file_name in file_names:
    data = np.loadtxt(file_name, delimiter=",", skiprows=2)
    voltage_freq_scale_minima.append(np.min(data[:, 1]))

avg_min_voltage = np.average(voltage_freq_scale_minima)
avg_min_voltage_error = np.std(voltage_freq_scale_minima)

print(f"Avg freq scale voltage minima: {avg_min_voltage:.2f} +/- {avg_min_voltage_error:.2f} V")

angular_sweep_file_name = f"{path_prefix}/spherical_angular_sweep_4970_Hz.csv"
data = np.loadtxt(angular_sweep_file_name, delimiter=",", skiprows=2)
voltage_freq_scale = data[:, 1]
avg_voltage = np.mean(voltage_freq_scale)
voltage_error = np.std(voltage_freq_scale)
print(f"Avg 4970 Hz voltage: {avg_voltage:.3f} +/- {voltage_error:.3f} V")

hz_per_volt = 4970 / (avg_voltage - avg_min_voltage)
delta_hz = 10
delta_denominator = voltage_error + avg_min_voltage_error
hz_per_volt_error = hz_per_volt * math.sqrt((delta_hz / 4970) ** 2 + (delta_denominator / (avg_voltage - avg_min_voltage) ** 2))
print(f"Hz per volt: {hz_per_volt:.0f} +/- {hz_per_volt_error:.0f} Hz")
