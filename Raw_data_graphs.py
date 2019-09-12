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
sub = 100
fish = fish_names[2]
for fish in (fish_names):
    mat_files = helpers.get_mat_files(fish, helpers.RECORDING_PATH16)
    file = mat_files[2]
    shift = 0
    for file in mat_files[0:4]:
        data = helpers.load_mat(file)
        file_name = helpers.path_to_name(file)
        sub_data = data[::sub]
        sampling_frequency = helpers.MAT_FREQUENCY/sub
        t_max = int(len(data) / helpers.MAT_FREQUENCY)
        x = np.arange(0, t_max, 1 / sampling_frequency)
        y = sub_data
        yf = fft(y)
        xf = np.linspace(0.0, 1.0 / (2.0 * 1 / sampling_frequency), int(len(x) / 2))
        power = 2.0/len(xf) * np.abs(yf[0:int(len(xf))])
        plt.plot(xf, shift+power/10)
        shift = shift + 1
        plt.grid()
        plt.ylabel('Amplitude')
        plt.xlabel('Frequency ')
        plt.xlim(0,6000)
        plt.title('FFT ' + file_name )
    helpers.save_figure(join(helpers.SAVE_PATH, fish), 'FFT', fish)
    plt.close()


