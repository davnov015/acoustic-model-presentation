import csv
from util import get_tube_file_name, tube_run_count, path_prefix


run_count = 55
source_file_path = "data/export.csv"
col_count = 4   # Columns per data set



file_data = []

####
# Load data
####

with open(source_file_path, mode='r') as source_file:
    csv_reader = csv.reader(source_file, delimiter=',')
    for row in csv_reader:
        file_data.append(row)

def write_csv_file(file_path, col_offset, col_count, index):
    with open(f"{path_prefix}/{file_path}", mode='w') as dest_file:
        csv_writer = csv.writer(dest_file, delimiter=',')
        col_i_start = index * col_count + col_offset
        col_i_end = col_i_start + col_count
        for row in file_data:
            dest_row = row[col_i_start:col_i_end]
            if not dest_row[1:][0] or len(dest_row[1:][0]) == 0:
                continue
            csv_writer.writerow(dest_row[1:])   # Exclude first column (time stamps)

####
# Write tube data files
####

for tube_run_i in range(tube_run_count):
    dest_file_name = get_tube_file_name(tube_run_i)
    write_csv_file(dest_file_name, 0, col_count, tube_run_i)


####
# Write spherical resonator static freq sweep
####

offset = tube_run_count * col_count
dest_file_name = "spherical_frequency_sweep.csv"
write_csv_file(dest_file_name, offset, col_count, 0)

####
# Write spherical resonator angular sweep
####

dest_file_name = "spherical_angular_sweep_4970_Hz.csv"
write_csv_file(dest_file_name, offset, col_count, 1)

####
# Angular frequency sweep
####

offset = 15 * col_count
angle_per_sweep = 10
for sweep_i in range(360 // angle_per_sweep):
    angular_position = sweep_i * angle_per_sweep
    dest_file_name = f"spherical_frequency_sweep_angle_{angular_position}.csv"
    write_csv_file(dest_file_name, offset, col_count, sweep_i)

####
# Detailed angular frequency sweep
####

offset = 52 * col_count
angle_per_sweep = 20
for sweep_i in range(3):
    angular_position = sweep_i * angle_per_sweep
    dest_file_name = f"spherical_freq_sweep_near_resonance_angle_{angular_position}.csv"
    write_csv_file(dest_file_name, offset, col_count, sweep_i)

