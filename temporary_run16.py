import helpers
from lewisfunctions.frequency import calculate_frequency
#from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt


fish_names = helpers.get_all_fish(helpers.RECORDING_PATH16)
indexes = []
fish = fish_names[1]
for fish in fish_names:
    mat_files = helpers.get_mat_files(fish, helpers.RECORDING_PATH16)
    file = mat_files[1]
    for file in mat_files[3:8]:
        raw_data = helpers.load_mat(file)
        signal_length = len(raw_data)
        data = np.array(raw_data)
        data = data[np.isfinite(data)]
        EOD = data - np.mean(data)
        sampling_frequency = helpers.MAT_FREQUENCY
        t_max = signal_length / helpers.MAT_FREQUENCY
        time_array = np.arange(0, t_max-1/sampling_frequency, 1 / sampling_frequency)  # IMPLEMENT IN HELPERS
        threshold = max(EOD)/2 #-0.08
        [xf, power] = helpers.compute_fft(EOD, 10, sampling_frequency)
        fft = [xf, power]
        f_estimate = power.argmax()

        f_estimate = calculate_frequency(EOD[::20], sampling_frequency/20, method='spectral')
        frequencies = calculate_frequency(EOD, sampling_frequency, estimated_frequency=f_estimate[0],
                                          crossing_threshold=threshold ,method='median', ascending=True)
        cv = '{:.2e}'.format(np.std(frequencies) / np.mean(frequencies))
        print(cv)
        print(np.mean(frequencies))

        #Saving the results
        file_name = helpers.path_to_name(file)
        helpers.save_results(frequencies, fish, file_name, 'frequency')
        helpers.save_results(fft, fish, file_name + '_fft', 'fft')