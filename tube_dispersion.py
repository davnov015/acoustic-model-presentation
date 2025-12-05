from matplotlib import pyplot as plt
import numpy as np
from tube_data import TubeData
from scipy.optimize import curve_fit
from fit_util import linear_fit


for tube_run_i in range(0, TubeData.tube_run_count):
    tube_data = TubeData(tube_run_i)

    popt, pcov = curve_fit(linear_fit, tube_data.wavenumber, tube_data.angular_frequency)
    k_line = np.linspace(0, tube_data.wavenumber[-1], 1000)
    plt.plot(k_line, linear_fit(k_line, *popt), label=rf"Fit: $v_g = {popt[0]:.2f}; b = {popt[1]:.2f}$")
    plt.scatter(tube_data.wavenumber, tube_data.angular_frequency)
    plt.xlabel("Wavenumber (m$^{-1}$)")
    plt.ylabel("Angular Frequency (rad/s)")
    plt.title(f"Tube Run {tube_run_i} Dispersion Relation (L = {tube_data.tube_length} cm; Iris Count = {tube_data.iris_count})")
    plt.legend()
    plt.show()
    print(f"v = {1 / tube_data.wavenumber[0] * tube_data.angular_frequency[0]}")
    print(popt)
    print(tube_data.wavenumber)
    print(tube_data.angular_frequency)

