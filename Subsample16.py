import helpers
from lewisfunctions.frequency import calculate_frequency
#from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt


fish_names = helpers.get_all_fish(helpers.RECORDING_PATH16)
indexes = []
fish = fish_names[0]
for fish in (fish_names):
    mat_files = helpers.get_mat_files(fish, helpers.RECORDING_PATH16)
    file = mat_files[0]
    for file in mat_files:
        data = helpers.load_mat(file)
        sampling_frequency = helpers.MAT_FREQUENCY
        step = 2
        step_size = np.size(data) / step
        i = 1
        #EOD = data
        for i in range(0, int(step)):
            sub_data = data[int(i * step_size): int((i + 1) * step_size)]
            sub_sampling = 1
            EOD = sub_data[::sub_sampling]
            sampling_frequency = helpers.MAT_FREQUENCY / sub_sampling
            t_max = int(len(data) / helpers.MAT_FREQUENCY)
            time = t_max / step
            time_array = np.arange(0, time-1/sampling_frequency, 1 / sampling_frequency)  # IMPLEMENT IN HELPERS
            threshold = max(data)/2
            fest = calculate_frequency(EOD[::20], sampling_frequency/20, method='spectral')
            frequencies = calculate_frequency(EOD, sampling_frequency, estimated_frequency=fest[0], crossing_threshold=threshold/2, method='median',ascending=True)
            cv = '{:.2e}'.format(np.std(frequencies) / np.mean(frequencies))

            file_name = helpers.path_to_name(file)
            helpers.save_results(frequencies, fish, file_name)

