import helpers
from lewisfunctions.frequency import calculate_frequency
#from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt


fish_names = helpers.get_all_fish(helpers.RECORDING_PATH16)
indexes = []
fish = fish_names[2]
for fish in fish_names:
    mat_files = helpers.get_mat_files(fish, helpers.RECORDING_PATH16)
    file = mat_files[8]
    for file in mat_files:
        print(file)
        raw_data = helpers.load_mat(file)
        signal_length = len(raw_data)
        EOD = helpers.cleaning_data(raw_data)

        sampling_frequency = helpers.MAT_FREQUENCY
        #t_max = signal_length / helpers.MAT_FREQUENCY
        #time_array = np.arange(0, t_max-1/sampling_frequency, 1 / sampling_frequency)  # IMPLEMENT IN HELPERS
        time = helpers.create_time(signal_length-1, style='MAT')

        threshold = max(EOD)/2 #-0.08
        [xf, power] = helpers.compute_fft(EOD, 60, sampling_frequency)
        f_estimate = 1.2*power.argmax()

        #f_estimate = calculate_frequency(EOD[::20], sampling_frequency/20, method='spectral')

        frequencies = calculate_frequency(EOD, sampling_frequency, estimated_frequency=f_estimate,
                                          crossing_threshold=threshold, temporal_threshold= 0.05, method='median', ascending=True)
        cv = '{:.2e}'.format(np.std(frequencies) / np.mean(frequencies))
        print(cv)
        print(np.mean(frequencies))

        file_name = helpers.path_to_name(file)

        frequency_info = [frequencies, cv, threshold]
        helpers.save_results(frequency_info, fish, file_name, 'frequency')

        fft = [xf, power]
        helpers.save_results(fft, fish, file_name + '_fft', 'fft')