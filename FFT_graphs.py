import matplotlib.pyplot as plt
import numpy as np
import helpers
from os.path import join

fish_names = helpers.get_all_fish(helpers.RECORDING_PATH16) # CHANGE TO RECORDING_PATH8 for 8 bits files
indexes = []
fish = fish_names[1]
levels = 3

mat_files = np.array(helpers.get_mat_files(fish, helpers.RECORDING_PATH16))
fft_files = helpers.get_npy_files(fish, helpers.SAVE_PATH, 'fft')
counter = 0
shift = 0
set = 1

for ind in range(len(fft_files)):
    if counter <= 3:
        counter += 1
        file_name = helpers.path_to_name(fft_files[0])
        xf, power = helpers.load_npy(fft_files[0])
        plt.plot(xf, shift + power / np.max(power))
        shift = shift + 1.2
        fft_files.pop(0)

    if counter == 3:
        shift = 0
        counter = 0
        plt.title('FFT ' + fish + str(set))
        plt.grid()
        plt.xlim(0, 6000)
        plt.ylabel('Amplitude')
        plt.xlabel('Frequency ')
        helpers.save_figure(join(helpers.SAVE_PATH, fish), 'FFT for set ' + str(set), fish, file_name, 'FFT_graphs')
        plt.close()
        set += 1

    elif ((len(fft_files) == 0) and counter == 2) or ((len(fft_files) == 0) and counter == 1):
        print('Here?')
        plt.ylabel('Amplitude')
        plt.xlabel('Frequency ')
        plt.grid()
        plt.xlim(0, 6000)
        plt.title('FFT ' + fish + str(set))
        helpers.save_figure(join(helpers.SAVE_PATH, fish), 'FFT for set ' + str(set), fish, file_name, 'FFT_graphs')
        plt.close()



