import math

import numpy as np

delta_index = 100

def frequency_to_index_map(frequency: np.typing.NDArray, index: int):
    assert frequency.size > index
    assert frequency.size > index and frequency.size > delta_index
    if frequency.size - delta_index <= index:
        index = index - delta_index

    delta_f = abs(frequency[index + delta_index] - frequency[index])
    return delta_index / delta_f

def window_size_function(frequency: np.typing.NDArray, index: int, frequency_window_size: int) -> int:
    dIdF = frequency_to_index_map(frequency, index)
    if math.isinf(dIdF):
        return delta_index
    return int(frequency_window_size * dIdF)

def find_peaks(data: np.typing.NDArray, frequency: np.typing.NDArray, frequency_window_size: int, frequency_window_offset: int = 0):
    peaks = []
    next_window_size = window_size_function(frequency, 0, frequency_window_size)
    next_window_offset = window_size_function(frequency, 0, frequency_window_offset)
    data_index = 0
    delta_index_cycle = False
    while data_index + next_window_size <= data.size:
        window_start = data_index + next_window_offset
        window_end = window_start + next_window_size
        data_index = window_end
        if data_index >= data.size:
            break
        next_window_size = window_size_function(frequency, data_index, frequency_window_size)
        if next_window_size == delta_index:
            data_index += delta_index
            delta_index_cycle = True
            continue
        next_window_offset = window_size_function(frequency, data_index, frequency_window_offset)
        if delta_index_cycle:
            delta_index_cycle = False
            continue
        window = data[window_start:window_end]
        max_index = np.argmax(window)
        max_value = window[max_index]
        window_edge_offset = 3
        if max_index < window_edge_offset or max_index > frequency_window_size - window_edge_offset:
            continue
        if max_value < 0.05:
            continue
        # Lookahead check
        failure = False
        next_window_range = next_window_size // 5
        if data_index + next_window_range <= data.size:
            for i in range(next_window_range):
                if max_value < data[window_end + i]:
                    failure = True
                    break
        if not failure:
            max_pos = window_start + max_index
            peaks.append(max_pos)

    if frequency_window_offset == 0:
        new_peaks = np.array([], dtype=np.int64)
        for i in range(1, 20):
            fresh_peaks = find_peaks(data, frequency, frequency_window_size, i * frequency_window_size // 10)
            new_peaks = np.union1d(new_peaks, fresh_peaks)
        peaks = np.union1d(peaks, new_peaks)
        # bins = np.linspace(0, data.size - 1, data.size // 100)
        # frequencies, _ = np.histogram(peaks, bins=bins, density=False)
        # assert np.where(frequencies > 1)[0].size == 0, "Clumping of peak values detected!"
        return peaks
    return np.array(peaks, dtype=np.int64)
