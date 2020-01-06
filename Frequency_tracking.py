import helpers
import numpy as np
import matplotlib.pyplot as plt
from os.path import join

lowrez = True
frequencies =[]
marker_ind = []
lowrez_index = []
highrez_index = []
fish_names = helpers.get_all_fish(helpers.SAVE_PATH)
fish = fish_names[4]

mat_files = helpers.get_mat_files(fish, helpers.RECORDING_PATH16)
[lowrez_index ,highrez_index ] = helpers.sort_files(mat_files)

if lowrez is True:
    file_number = lowrez_index
else:
file_number = highrez_index

for index in file_number:
    npy_files = helpers.get_npy_files(fish, helpers.SAVE_PATH, 'frequency')
    file_name = helpers.path_to_name(npy_files[index])
    [frequency, cv, threshold] = helpers.load_npy(npy_files[index])
    cycle_time = np.cumsum(1. / frequency)
    plt.figure('Frequency with time')
    plt.plot(cycle_time, frequency, '.')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [s]')
    plt.title('Frequency variation in time for ' + file_name + ' CV = ' + str(cv))
    helpers.save_figure(join(helpers.SAVE_PATH, fish), 'Frequency in time for ', fish, file_name)
    plt.close()
    if lowrez is True:
        frequencies = np.append(frequencies, frequency)
        marker_ind = np.append(marker_ind, len(frequency))
        marker_index = np.cumsum(marker_ind)

if lowrez is True :
    sum_cycle_time = np.cumsum(1. / frequencies)
    plt.figure('Frequency with time')
    plt.plot(sum_cycle_time, frequencies, '.')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [s]')
    plt.title('Frequency variation in time for ' + fish )
    for xc in marker_index[:-1]:
        plt.axvline(x=sum_cycle_time[int(xc)], color='k', linestyle='--')
    for xc in marker_index[:-1:2]:
            plt.axvline(x=sum_cycle_time[int(xc)], color='r', linestyle='--')
    helpers.save_figure(join(helpers.SAVE_PATH, fish), 'Cumulatif frequency in time for ', fish, file_name)
    plt.close()



