import scipy.io as sio
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
import helpers
from os.path import join

#from tqdm import tqdm
import csv
import pandas as pd
import os

fish_names = helpers.get_all_fish(helpers.RECORDING_PATH16) # CHANGE TO RECORDING_PATH8 for 8 bits files
indexes = []
sub = 50
fish = fish_names[6]
for fish in (fish_names):
    mat_files = np.array(helpers.get_mat_files(fish, helpers.RECORDING_PATH16))
    fft_files = helpers.get_npy_files(fish , helpers.SAVE_PATH, 'fft')
    file = mat_files[3]
    shift = 0
    for numb in range(15,19):
        print(numb)
        file = mat_files[numb]
        file_name = helpers.path_to_name(file)
        [xf, power] = helpers.load_npy(fft_files[numb])
        plt.plot(xf, shift+power/np.max(power))
        shift = shift + 1.2
        plt.grid()
        plt.ylabel('Amplitude')
        plt.xlabel('Frequency ')
        plt.xlim(0,6000)
        plt.title('FFT ' + file_name )
    helpers.save_figure(join(helpers.SAVE_PATH, fish), 'FFT 3', fish, file_name)
    plt.close()


