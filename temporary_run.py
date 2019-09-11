import helpers
from lewisfunctions.frequency import calculate_frequency
from tqdm import tqdm
import numpy as np

fish_names = helpers.get_all_fish(helpers.RECORDING_PATH)
indexes = []
for fish in tqdm(fish_names):
    npy_files = helpers.get_high_frequency_files(fish, helpers.RECORDING_PATH)
    for file in tqdm(npy_files):
        data = helpers.load_npy(file)
        data = np.array(data, dtype='int')
        EOD = data - min(data)
        max_EOD = max(EOD)
        thresholds = []
        all_frequencies = []
        threshold = max_EOD/10
        cvs = []
        time = helpers.create_time(len(data), style='NPY')

        for i in tqdm(range(1, 3)):
            threshold = threshold + max_EOD / 10
            thresholds.append(threshold)
            time = helpers.create_time(len(EOD), style='NPY')
            fest = calculate_frequency(EOD[::20], helpers.NPY_FREQUENCY/20, method='spectral')
            frequencies = calculate_frequency(EOD, helpers.NPY_FREQUENCY, estimated_frequency=fest[0], crossing_threshold=threshold, method='median')
            all_frequencies.append(frequencies)
            cv = '{:.2e}'.format(np.std(frequencies) / np.mean(frequencies))
            cvs.append(cv)

        index = np.argmin(np.array(cvs).astype(np.float))
        best_frequencies = all_frequencies[index]
        indexes.append(index)
        file_name = helpers.path_to_name(file)
        helpers.save_results(best_frequencies, fish, file_name)

np.save('List of best indexes', indexes)

