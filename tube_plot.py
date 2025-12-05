import numpy as np
from matplotlib import pyplot as plt
from tube_data import TubeData


for tube_run_i in range(TubeData.tube_run_count):
    tube_data = TubeData(tube_run_i)

    plt.plot(tube_data.ma_frequency, tube_data.amplitude_ma, color="red")
    plt.scatter(tube_data.peak_frequencies, tube_data.peak_amplitudes, marker="x", linewidths=2, color="green")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude (V)")
    plt.title(f"Tube Run {tube_run_i}")
    plt.show()

    print(f"Run {tube_run_i}: {tube_data.resonance_n}")
