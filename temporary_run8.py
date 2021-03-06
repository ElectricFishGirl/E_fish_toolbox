import helpers
from lewisfunctions.frequency import calculate_frequency
#from tqdm import tqdm
import numpy as np

fish_names = helpers.get_all_fish(helpers.RECORDING_PATH8)
indexes = []
fish = fish_names[1]
for fish in tqdm(fish_names):
    npy_files = helpers.get_high_frequency_files(fish, helpers.RECORDING_PATH8)
    file = npy_files[0]
    for file in tqdm(npy_files):
        data = helpers.load_npy(file)
        data = np.array(data, dtype='int')
        sampling_frequency = helpers.NPY_FREQUENCY
        EOD = data - np.mean(data)
        t_max = int(len(data) / helpers.NPY_FREQUENCY)
        time_array = np.arange(0, t_max-1/sampling_frequency, 1 / sampling_frequency)  # IMPLEMENT IN HELPERS
        threshold = max(data)/2
        fest = calculate_frequency(EOD[::20], sampling_frequency/20, method='spectral')
        frequencies = calculate_frequency(EOD, sampling_frequency, estimated_frequency=fest[0],
                                          crossing_threshold=threshold/2, method= 'median',ascending=True )
        cv = '{:.2e}'.format(np.std(frequencies) / np.mean(frequencies))

        file_name = helpers.path_to_name(file)
        helpers.save_results(frequencies, fish, file_name)
