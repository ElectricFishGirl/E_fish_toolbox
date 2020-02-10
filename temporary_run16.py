import helpers
from lewisfunctions.frequency import calculate_frequency
import numpy as np
from os.path import join
import os
import matplotlib.pyplot as plt
fish_names = helpers.get_all_fish(helpers.RECORDING_PATH16)
fish = fish_names[2]
highrez = []
lowrez = []
mat_files = helpers.get_mat_files(fish, helpers.RECORDING_PATH16)
[lowrez,highrez ] = helpers.sort_files(mat_files)

file = mat_files[0]
for index in highrez:
    file = mat_files[index]
    print(file)
    raw_data = helpers.load_mat(file)
    signal_length = len(raw_data)
    EOD = helpers.cleaning_data(raw_data)
    sampling_frequency = helpers.MAT_FREQUENCY
    time = helpers.create_time(signal_length-1, style='MAT')
    threshold =  np.max(EOD)/3

    [xf, power] = helpers.compute_fft(EOD[:len(EOD)//100], 1, sampling_frequency)
    f_estimate = 2.*power.argmax()

    frequencies = calculate_frequency(EOD, sampling_frequency, estimated_frequency=f_estimate,
                                      crossing_threshold=threshold, temporal_threshold= 0.05,  method='median', ascending=True)
    cv = '{:.2e}'.format(np.std(frequencies) / np.mean(frequencies))
    print(cv)
    print(np.mean(frequencies))

    file_name = helpers.path_to_name(file)

    frequency_info = [frequencies, cv, threshold]
    helpers.save_results(frequency_info, fish, file_name, 'frequency')
    fft = [xf, power]
    helpers.save_results(fft, fish, file_name + '_fft', 'fft')

for index in lowrez:
    file = mat_files[index]
    print(file)
    raw_data = helpers.load_mat(file)
    signal_length = len(raw_data)
    EOD = helpers.cleaning_data(raw_data)
    sampling_frequency = 500000
    threshold = np.max(EOD)/3
    f_estimate = 800
    frequencies = calculate_frequency(EOD, sampling_frequency, estimated_frequency=f_estimate,
                                     crossing_threshold=threshold, temporal_threshold=0.05,
                                     method='median', ascending=True)
    cv = '{:.2e}'.format(np.std(frequencies) / np.mean(frequencies))
    print(cv)
    print(np.mean(frequencies))
    #[xf, power] = helpers.compute_fft(EOD[len(EOD)//2:len(EOD)//2+len(EOD)//100], 1, sampling_frequency)

    file_name = helpers.path_to_name(file)
    frequency_info = [frequencies, cv, threshold]
    helpers.save_results(frequency_info, fish, file_name, 'frequency')
    #fft = [xf, power]
    #helpers.save_results(fft, fish, file_name + '_fft', 'fft')