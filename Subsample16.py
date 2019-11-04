import helpers
import numpy as np


fish_names = helpers.get_all_fish(helpers.RECORDING_PATH16)
indexes = []
fish = fish_names[6]
sampling_frequency = 500000
step = 12 # 15 seconds
for fish in (fish_names):
    mat_files = helpers.get_mat_files(fish, helpers.RECORDING_PATH16)
    file = mat_files[19]
    for file in mat_files:
        raw_data = helpers.load_mat(file)
        EOD = helpers.cleaning_data(raw_data)
        step_size = np.size(EOD) / step
        i = 0
        for i in range(0, int(step)):
            sub_data = EOD[int(i * step_size): int((i + 1) * step_size)]
            sub_sampling = 1
            sub_EOD = sub_data[::sub_sampling]
            [xf, power] = helpers.compute_fft(sub_EOD, 1, sampling_frequency)
            file_name = helpers.path_to_name(file)
            fft = [xf, power]
            helpers.save_results(fft, fish, file_name + '_fft_' + str(i), 'fft')