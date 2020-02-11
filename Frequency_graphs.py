import helpers
import numpy as np
import matplotlib.pyplot as plt
from os.path import join

fish_names = helpers.get_all_fish(helpers.SAVE_PATH)
fish = fish_names[9]

CVs = []
average_frequencies = []
file_names = []
lowrez_index = []
highrez_index = []

lowrez = False
frequencies = []


npy_files = helpers.get_npy_files(fish, helpers.SAVE_PATH, 'frequency')
fft_files = helpers.get_npy_files(fish, helpers.SAVE_PATH, 'fft')
mat_files = helpers.get_mat_files(fish, helpers.RECORDING_PATH16)
[lowrez_index, highrez_index] = helpers.sort_files(mat_files)
file_number = highrez_index

for numb in file_number:
    index = file_number.index(numb)
    raw_data = helpers.load_mat(mat_files[numb])
    data = np.array(raw_data)
    data = data[np.isfinite(data)]
    EOD = data - np.mean(data)
    file_name = helpers.path_to_name(mat_files[numb])
    [frequency, cv, threshold] = helpers.load_npy(npy_files[numb])

    time_array = helpers.create_time(len(raw_data)-1, style='MAT')
    cycle_time = np.cumsum(1. / frequency)

    [xf, power] = helpers.load_npy(fft_files[index])
    fft_main = 2*power.argmax()

    fig = plt.figure('Explore V1 ' + file_name )
    ax1 = fig.add_subplot(221)
    ax1.plot(time_array[::50] , EOD[1::50])
    ax1.set_title('Full data')

    ax2 = fig.add_subplot(222)
    ax2.plot(time_array[0:675000] , EOD[0:675000]) # shows 5 cycles
    ax2.axhline(threshold, color='r')
    ax2.set_title('Waveform')

    ax3 = fig.add_subplot(223)
    ax3.plot(xf,  power/np.max(power))
    ax3.set_title('FFT' + ' Fundamental at ' + str(fft_main) + 'HZ')
    ax3.set_ylabel('Amplitude')
    ax3.set_xlabel('Frequency ')
    ax3.set_xlim(0, 3000)

    ax4 = fig.add_subplot(224)
    ax4.plot(cycle_time, frequency, '.')
    ax4.set_title('Frequency with time' + ' CV = ' + str(cv))

    helpers.save_figure(join(helpers.SAVE_PATH, fish), 'Explore V1.1 for ', fish,  file_name, 'Explore_graphs')
    plt.close()

    #Analysis plot

    fig = plt.figure('Analysis V1 ' + file_name)

    ax1 = fig.add_subplot(221)
    ax1.hist((1./frequency)*1e3, bins = 20)
    ax1.set_title('Histogram of period [ms]' + ' CV = ' + str(cv))

    ax2 = fig.add_subplot(222)
    m13 = frequency
    m12 = np.roll(m13, 1)  # shift by one
    color = np.sort(m13)
    ax2.scatter(m13, m12, c=color, marker='.')
    ax2.set_title('Shifted frequency [Hz]')
    ax2.axis('equal')

    ax3 = fig.add_subplot(224)
    period = (1. / frequency) * 1e3
    ax3.acorr(period - period.mean(), usevlines=True, maxlags=10, normed=True, lw=2)
    ax3.grid(True)
    ax3.axhline(0, color='black', lw=2)
    ax3.set_title('Auto-Correlation')

    ax4 = fig.add_subplot(223)
    ax4.plot(cycle_time, (1./frequency)*1e3, '.')
    ax4.set_xlabel('Time [s]')
    ax4.set_ylabel('Period [ms]')
    helpers.save_figure(join(helpers.SAVE_PATH, fish), 'Analysis V1.1 for ', fish, file_name, 'Analysis_graphs')
    plt.close()

