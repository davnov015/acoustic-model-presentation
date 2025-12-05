from matplotlib import pyplot as plt
import numpy as np
from tube_data import TubeData
from scipy.optimize import curve_fit
from fit_util import linear_fit
from util import iris_count


no_iris_indices = [index for index, value in enumerate(iris_count) if value == 0]

for tube_run_i in range(TubeData.tube_run_count):
    tube_data = TubeData(tube_run_i)

    popt, pcov = curve_fit(linear_fit, tube_data.wavenumber, tube_data.angular_frequency, sigma=tube_data.angular_frequency_delta)
    v_g_delta = np.sqrt(pcov[0][0])
    k_line = np.linspace(0, tube_data.wavenumber[-1], 1000)
    plt.figure(figsize = (7, 5))
    plt.plot(k_line, linear_fit(k_line, *popt), label=rf"Fit: $v_g = {popt[0]:.0f} \pm {v_g_delta:.0f}$")
    plt.errorbar(tube_data.wavenumber, tube_data.angular_frequency, yerr=tube_data.angular_frequency_delta, fmt="x", capsize=5, ecolor="red", label="Resonance Points")
    plt.xlabel("Wavenumber (m$^{-1}$)")
    plt.ylabel("Angular Frequency (rad/s)")
    plt.title(f"Tube Run {tube_run_i} Dispersion Relation (L = {tube_data.tube_length} cm; Iris Count = {tube_data.iris_count})")
    plt.legend()
    plt.show()
    print(f"v = {1 / tube_data.wavenumber[0] * tube_data.angular_frequency[0]}")
    print(popt)
    print(tube_data.wavenumber)
    print(tube_data.angular_frequency)

