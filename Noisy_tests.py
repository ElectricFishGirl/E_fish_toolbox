import helpers
from lewisfunctions.frequency import calculate_frequency
from scipy.signal import correlate
#from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
fish_names = helpers.get_all_fish(helpers.RECORDING_PATH16)
indexes = []
fish = fish_names[1]
for fish in fish_names:
    mat_files = helpers.get_mat_files(fish, helpers.RECORDING_PATH16)
    file = mat_files[10]
    for file in mat_files[4:10]:
        print(file)
        raw_data = helpers.load_mat(file)
        signal_length = len(raw_data)
        EOD = helpers.cleaning_data(raw_data)

        sampling_frequency = 500000
        t_max = signal_length / 500000
        time_array = np.arange(0, t_max-1/500000, 1 / 500000)  # IMPLEMENT IN HELPERS

        threshold = 0
        f_estimate = 800

        frequencies = calculate_frequency(EOD, sampling_frequency, estimated_frequency=f_estimate,
                                          crossing_threshold=threshold, temporal_threshold= 0.05, method='median', ascending=False)
        cv = '{:.2e}'.format(np.std(frequencies) / np.mean(frequencies))
        print(cv)
        print(np.mean(frequencies))


        file_name = helpers.path_to_name(file)

        frequency_info = [frequencies, cv, threshold]
        helpers.save_results(frequency_info, fish, file_name, 'frequency')


npy_files = helpers.get_npy_files(fish, helpers.SAVE_PATH, 'frequency')

frequencies = []

for i in range(len(npy_files)):
    [frequency, cv, threshold] = helpers.load_npy(npy_files[i])
    frequency = frequency.tolist()
    frequencies.extend(frequency)

size = np.size(frequencies)/len(npy_files)

markers = [ size* i  for i in range(len(npy_files))  ]

plt.plot(frequencies, '.')
for xc in markers[::2]:
    plt.axvline(x=xc , c = 'k')