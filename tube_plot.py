import numpy as np
from matplotlib import pyplot as plt

from fit_util import moving_avg
from util import get_all_tube_file_names
from peak_detector import find_peaks

file_names = get_all_tube_file_names(include_iris=True, include_path_prefix=True)

data = np.loadtxt(file_names[0], delimiter=",", skiprows=2)
frequency = data[:, 1]  # Initially in volts
amplitude = data[:, 2]

reordering = np.argsort(frequency)
frequency = frequency[reordering]
amplitude = amplitude[reordering]

hz_per_volt = 1000
frequency += 2.04
frequency *= hz_per_volt

# Check for a flat start and remove it
filter = (amplitude > 0.1) | (frequency > 500)
frequency = frequency[filter]
amplitude = amplitude[filter]

f_index_space = np.linspace(0, frequency.size - 1, frequency.size)


plt.figure(figsize=(10, 5))
f_space = np.linspace(0, frequency.size - 1, frequency.size)

plt.scatter(frequency, amplitude, marker=".")

avg_length = 10
amplitude_ma = moving_avg(amplitude, avg_length)
ma_frequency = frequency[(avg_length - 1) * 2:]
amplitude_ma = amplitude_ma[avg_length - 1:]

ma_f_space = f_space[(avg_length - 1) * 2:]

peaks = find_peaks(amplitude_ma, ma_frequency, 400)


plt.plot(ma_frequency, amplitude_ma, color="red")
plt.scatter(ma_frequency[peaks], amplitude_ma[peaks], marker="x", color="green")
plt.show()

