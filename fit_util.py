import numpy as np


def coefficient_of_determination(y_true, y_pred):
    """
    Calculate the coefficient of determination (R^2) for the prediction.
    :param y_true: The actual values.
    :param y_pred: The predicted values.
    :return: The coefficient of determination.
    """
    correlation_matrix = np.corrcoef(y_true, y_pred)
    correlation = correlation_matrix[0, 1]
    return correlation ** 2

def moving_avg(series: np.array, window_size: int) -> np.array:
    sum_series = np.cumsum(series)
    sum_series[window_size:] = sum_series[window_size:] - sum_series[:-window_size]
    return sum_series[window_size - 1:] / window_size

def moving_std(series: np.array, window_size: int) -> np.array:
    deviation = series[window_size - 1:] - moving_avg(series, window_size)
    return np.sqrt(moving_avg(deviation ** 2, window_size))

def bucket_sort(v: np.array, i: np.array, delta_v: float) -> (np.array, np.array, np.array, np.array):
    v_range = np.max(v) - np.min(v)
    bucket_count = int(v_range / delta_v)
    v_buckets = [[] for _ in range(bucket_count)]
    v_bucket_avgs = np.zeros(len(v_buckets))
    v_bucket_stds = np.zeros(len(v_buckets))
    i_buckets = [[] for _ in range(bucket_count)]
    i_bucket_avgs = np.zeros(len(i_buckets))
    i_bucket_stds = np.zeros(len(i_buckets))
    for j in range(len(v)):
        v_value = v[j]

        bucket_index = find_bucket(v_buckets, v_value, delta_v)
        v_buckets[bucket_index].append(v_value)
        v_bucket_avgs[bucket_index] = np.mean(v_buckets[bucket_index])
        v_bucket_stds[bucket_index] = np.std(v_buckets[bucket_index])

        i_buckets[bucket_index].append(i[j])
        i_bucket_avgs[bucket_index] = np.mean(i_buckets[bucket_index])
        i_bucket_stds[bucket_index] = np.std(i_buckets[bucket_index])

    # Discard empty buckets
    empty_entries = []
    for j in range(len(v_buckets)):
        if len(v_buckets[j]) == 0:
            empty_entries.append(j)
    # No need to remove the empty buckets themselves, they're discarded anyway
    # v_buckets = [v_buckets[i] for i in range(len(v_buckets)) if i not in empty_entries]
    # i_buckets = [i_buckets[i] for i in range(len(i_buckets)) if i not in empty_entries]
    v_bucket_avgs = np.delete(v_bucket_avgs, empty_entries)
    v_bucket_stds = np.delete(v_bucket_stds, empty_entries)
    i_bucket_avgs = np.delete(i_bucket_avgs, empty_entries)
    i_bucket_stds = np.delete(i_bucket_stds, empty_entries)
    return v_bucket_avgs, v_bucket_stds, i_bucket_avgs, i_bucket_stds


def find_bucket(buckets: list, value: float, delta_v: float) -> int:
    first_empty_bucket_index = None
    for k in range(len(buckets)):
        if len(buckets[k]):
            v_values = np.array(buckets[k])
            if np.any(v_values < value + delta_v) and np.any(v_values > value - delta_v):
                return k
        else:
            if first_empty_bucket_index is None:
                first_empty_bucket_index = k
            continue
    assert first_empty_bucket_index is not None, "Could not classify value"
    return first_empty_bucket_index

def chi_squared(data: np.array, model: np.array, sigma: np.array) -> float:
    return np.sum(((data - model) / sigma) ** 2)

linear_fit = lambda x, a, b: a*x + b
