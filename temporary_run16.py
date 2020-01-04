import helpers
import lewisfunctions
from lewisfunctions.frequency import calculate_frequency
from scipy.signal import correlate
#from tqdm import tqdm
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

fish_names = helpers.get_all_fish(helpers.RECORDING_PATH16)
fish = fish_names[2]
for fish in fish_names:
    mat_files = helpers.get_mat_files(fish, helpers.RECORDING_PATH16)
    file = mat_files[0]
    highrez = [0,1,2,3,7,8,9,12,13,14,17,18,19,22,23]
    lowrez = [4,5,6,10,11,15,16,20,21]
    for index in highrez:
        file = mat_files[index]
        print(file)
        raw_data = helpers.load_mat(file)
        signal_length = len(raw_data)
        EOD = helpers.cleaning_data(raw_data)
        sampling_frequency =helpers.MAT_FREQUENCY#500000  #
       # t_max = signal_length / 500000
       # time_array = np.arange(0, t_max-1/500000, 1 / 500000)  # IMPLEMENT IN HELPERS
        time = helpers.create_time(signal_length-1, style='MAT')

        threshold = np.max(EOD)/2 #-0.08

        [xf, power] = helpers.compute_fft(EOD, 60, sampling_frequency)
        f_estimate = 1.*power.argmax()


        frequencies = calculate_frequency(EOD, sampling_frequency, estimated_frequency=f_estimate,
                                          crossing_threshold=threshold, temporal_threshold= 0.05,  method='median', ascending=False)
        cv = '{:.2e}'.format(np.std(frequencies) / np.mean(frequencies))
        print(cv)
        print(np.mean(frequencies))

        file_name = helpers.path_to_name(file)

        frequency_info = [frequencies, cv, threshold]
        helpers.save_results(frequency_info, fish, file_name, 'frequency')
        fft = [xf, power]
        helpers.save_results(fft, fish, file_name + '_fft', 'fft')