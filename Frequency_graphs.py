import helpers
#from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
from os.path import join

CVs = []
average_frequencies = []
file_names = []
fish_names = helpers.get_all_fish(helpers.SAVE_PATH)
#Analysis_filename = 'Analysis_t11.csv'

fish = fish_names[0]
for fish in fish_names:
    npy_files = helpers.get_high_frequency_files(fish, helpers.SAVE_PATH)
    file = npy_files[0]
    for file in npy_files:
        data = helpers.load_mat(file)
        file_name = helpers.path_to_name(file)
        sampling_frequency = helpers.MAT_FREQUENCY
        t_max = len(data) / helpers.MAT_FREQUENCY
        x = np.arange(0, t_max, 1 / sampling_frequency)
        y = data
        yf = fft(y)
        xf = np.linspace(0.0, 1.0 / (2.0 * 1 / sampling_frequency), int(len(x) / 2))
        power = 2.0 / len(xf) * np.abs(yf[0:int(len(xf))])
        plt.plot(xf, shift + power / 10)
        shift = shift + 1
        plt.grid()
        plt.ylabel('Amplitude')
        plt.xlabel('Frequency ')
        plt.xlim(0, 3000)
        plt.title('FFT ' + file_name)

        frequency = helpers.load_npy(file)
        average_frequency = np.mean(frequency)
        period = 1. / frequency
        period_ms = period*1e3
        shifted_frequency = np.roll(frequency, 1)
        cycle_time = np.cumsum(period)
        cv = '{:.2e}'.format(np.std(frequency)/np.mean(frequency))
        file_name = helpers.path_to_name(file)
        file_names.append(file_name)
        average_frequencies.append(average_frequency)
        CVs.append(cv)
        #analysis = pd.DataFrame({'Fish_name': file_names, 'Average Frequency': average_frequencies, 'CV': CVs})
        #analysis.to_csv(Analysis_filename, index=False)

        fig = plt.figure("Explore V1")
        y = frequency - np.mean(frequency)
        # z = randomperiod - np.mean(randomperiod)
        ax1 = fig.add_subplot(221)
        ax1.acorr(y, usevlines=True, maxlags=50, normed=True, lw=2)
        ax1.grid(True)
        ax1.axhline(0, color='black', lw=2)
        ax1.set_title('Correlation')


        ax2 = fig.add_subplot(222)
        ax2.hist(frequency, bins=60)
        ax2.set_title('Histogram' + ' CV = ' + str(cv))


        m13 = frequency
        m12 = np.roll(m13, 1)  # shift by one
        color = np.sort(m13)
        ax3 = fig.add_subplot(223)
        ax3.scatter(m13, m12, c=color, marker='.')
        ax3.set_title('Shifted frequency')
        ax3.axis('equal')

        ax4 = fig.add_subplot(224)
        ax4.plot(cycle_time, frequency, '.')
        ax4.set_title('Frequency with time')


        helpers.save_figure(helpers.file_to_path(file), 'Analysis for ', fish,  file_name)
        plt.close()

        # fig = plt.figure("Analysis")
        # y = frequency - np.mean(frequency)
        # # z = randomperiod - np.mean(randomperiod)
        # ax1 = fig.add_subplot(221)
        # ax1.acorr(y, usevlines=True, maxlags=50, normed=True, lw=2)
        # ax1.grid(True)
        # ax1.axhline(0, color='black', lw=2)
        # ax1.set_title('Correlation')
        #
        #
        # ax2 = fig.add_subplot(222)
        # ax2.hist(frequency, bins=60)
        # ax2.set_title('Histogram' + ' CV = ' + str(cv))
        #
        #
        # m13 = frequency
        # m12 = np.roll(m13, 1)  # shift by one
        # color = np.sort(m13)
        # ax3 = fig.add_subplot(223)
        # ax3.scatter(m13, m12, c=color, marker='.')
        # ax3.set_title('Shifted frequency')
        # ax3.axis('equal')
        #
        # ax4 = fig.add_subplot(224)
        # ax4.plot(cycle_time, frequency, '.')
        # ax4.set_title('Frequency with time')
        #
        #
        # helpers.save_figure(helpers.file_to_path(file), 'Analysis for ', fish,  file_name)
        # plt.close()


        plt.figure('Frequency with time')
        plt.plot(cycle_time, frequency, '.')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [s]')
        plt.title('Frequency variation in time for ' + file_name + ' CV = ' + str(cv))
        helpers.save_figure(helpers.file_to_path(file), 'Frequency in time for ', fish, file_name)
        #helpers.save_figure('processed_data/All fish/Frequency tracking/', 'Frequency in time for ', file_name)
        plt.close()

        plt.figure('Histogram of frequencies')
        plt.hist(frequency, bins=40)
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('instances')
        plt.title('Histogram of frequencies for ' + file_name + ' CV = ' + str(cv))
        helpers.save_figure(helpers.file_to_path(file), 'Histogram of frequencies ', fish, file_name)  #saves each fish in its own folder
        #helpers.save_figure('processed_data/All fish/Histograms', 'Histogram of frequencies ', file_name)
        plt.close()
        #
        # plt.figure('Histogram of periods')
        # plt.hist(period_ms, bins=40)
        # plt.xlabel('Periods [ms]')
        # plt.ylabel('instances')
        # plt.title('Histogram of periods for ' + file_name + ' CV = ' + str(cv))
        # helpers.save_figure(helpers.file_to_path(file), 'Histogram of periods ', fish, file_name)  #saves each fish in its own folder
        # #helpers.save_figure('processed_data/All fish/Histograms', 'Histogram of periods ', file_name)
        # plt.close()
        #
        # plt.figure('Correlation')
        # color = np.sort(shifted_frequency)
        # plt.scatter(shifted_frequency, frequency, c=color, marker='.')
        # plt.ylabel('Frequency [Hz]')
        # plt.xlabel('Following frequency [Hz]')
        # plt.title('Correlation for ' + file_name + ' CV = ' + str(cv))
        # plt.axis('equal')
        # helpers.save_figure(helpers.file_to_path(file), 'Correlation for ', fish, file_name)
        # #helpers.save_figure('processed_data/All fish/Correlations/', 'Correlation for ', file_name)
        # plt.close()

#
# Analysis_t8 = pd.read_csv('Analysis_t8.csv')
# frequencies_t8 = np.array(Analysis_t8['Average Frequency'])
# cvs_t8 = np.array(Analysis_t8['CV'])
# plt.figure('Frequency ')
# plt.plot(frequencies_t8, '.', color='r')
# plt.figure('CV ')
# plt.plot(cvs_t8, '.', color='r')

