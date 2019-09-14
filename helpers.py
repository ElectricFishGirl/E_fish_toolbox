from glob import glob
import os
from os.path import join, split, isdir
import numpy as np
import matplotlib.pyplot as plt
import json
import scipy.io as sio
from scipy.fftpack import fft

RECORDING_PATH8 = '../../Recordings/8bits/'
RECORDING_PATH16 = '../../Recordings/16bits/'

SAVE_PATH = '../processed_data/'

MANIFEST_FILE = 'manifest.json'

NPY_FREQUENCY = 41666666.666
LONG_FREQUENCY = 10416666.666
MAT_FREQUENCY = 62500002

def get_all_fish(path):
    name_paths = glob(join(path, "*"))
    return [split(x)[-1] for x in name_paths]


def get_high_frequency_files(fish_name, path):
    return glob(join(path, fish_name, "*.npy"))

def get_mat_files(fish_name, path):
    return glob(join(path, fish_name, "*.mat"))

def load_npy(path):
    return np.load(path)

def load_mat(path):
    mat_file = sio.loadmat(path)
    weird_data = mat_file['A']
    stripper = []
    for i in range(len(weird_data)):
        stripper.append(weird_data[i][0])
    return stripper


def create_time(file_length, style='NPY'):
    switcher = {
        'NPY': 1. / NPY_FREQUENCY,
        'LONG': 1. / LONG_FREQUENCY,
        'MAT' : 1./ MAT_FREQUENCY
    }

    dt = switcher[style]

    return np.arange(file_length) * dt


def __make_dir_if_not_exist__(path):
    if not isdir(path):
        os.mkdir(path)


def path_to_name(path):
    return '.'.join(split(path)[-1].split('.')[:-1])


def file_to_path(path):
    return split(path)[0]


def save_results(frequencies, fish_name, file_name):
    save_path = join(SAVE_PATH, fish_name)
    __make_dir_if_not_exist__(save_path)

    np.save(join(save_path, file_name), frequencies)


def save_figure(path, plot_type, fish_name):
    save_path = join(SAVE_PATH, fish_name)
    __make_dir_if_not_exist__(save_path)
    plt.tight_layout()
    plt.savefig(join(path, plot_type + "_" + fish_name + ".jpg"))
    #plt.close()



def load_manifest():
    with open(MANIFEST_FILE, 'r') as f:
        manifest = json.load(f)

    return manifest

