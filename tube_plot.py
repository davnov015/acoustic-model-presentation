import numpy as np
from matplotlib import pyplot as plt
from tube_data import TubeData


for tube_run_i in range(0, TubeData.tube_run_count):
    tube_data = TubeData(tube_run_i)

    plt.plot(tube_data.ma_frequency, tube_data.amplitude_ma, color="red", label="Amplitude MA(10)")
    plt.scatter(tube_data.peak_frequencies, tube_data.peak_amplitudes, marker="x", linewidths=2, color="green", label="Resonance Point")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude (V)")
    plt.title(f"Tube Run {tube_run_i}: L = {tube_data.tube_length} cm; Iris Count = {tube_data.iris_count}")
    plt.grid(True)
    plt.legend()
    plt.show()

    print(f"Run {tube_run_i}: {tube_data.resonance_n}")
