
path_prefix = "data/output"

tube_run_count = 13
tube_lengths = [37.5, 30, 5, 20, 55, 60, 58.5, 57.5, 56.5, 60, 63.5, 62, 61]
iris_count = [0, 0, 0, 0, 0, 10, 7, 5, 3, 0, 7, 4, 2]
window_size = [400, 400, 700, 800, 150, 150, 100, 100, 100, 370, 200, 150, 400]
first_peak_n = [1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 2, 1, 1]

assert len(tube_lengths) == len(iris_count) == len(window_size) == len(first_peak_n) == tube_run_count

def get_tube_file_name(run_index: int, include_path_prefix=False):
    """
    Generate a tube-data CSV file name, including the tube length and iris count.
    :param run_index: The index of the tube experiment run.
    :param include_path_prefix: If set, the full path prefix will be included in the file name.
    :return: The file name.
    """
    prefix = path_prefix + "/" if include_path_prefix else ""
    return f"{prefix}tube_l_{tube_lengths[run_index]}_ir_{iris_count[run_index]}.csv"

def get_all_tube_file_names(include_iris=False, include_path_prefix=True):
    """
    Generate a list of tube-data CSV file names. Can include or exclude tubes with irises. Can generate the full path,
    or just a list of the file names.
    :param include_iris: If set, the tubes with irises will be included as well.
    :param include_path_prefix: If set, the full path prefix will be included in the file names.
    :return: A list of file names.
    """
    filter_condition = lambda index: (not include_iris and iris_count[index] == 0) or include_iris
    return [get_tube_file_name(index, include_path_prefix) for index in range(tube_run_count) if filter_condition(index)]
