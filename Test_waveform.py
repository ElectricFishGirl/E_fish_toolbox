import helpers
import numpy as np
import matplotlib.pyplot as plt
from lewisfunctions.frequency import calculate_frequency

data = helpers.load_npy('../Recordings/Calibration/FG_921_3.npy')

frequency = calculate_frequency(data, helpers.NPY_FREQUENCY, method='simple')
period = 1./frequency
"""""
sample_frequency = 41666666.666
sample_period = 1 / sample_frequency
#time = sample_period * np.arange(len(data))
time = helpers.create_time(len(data), style='NPY')

plt.plot(time[:1000000], -data[:1000000])
plt.plot([time[0], np.max(time[:1000000])], [threshold_1, threshold_1], 'k')
plt.plot([time[0], np.max(time[:1000000])], [threshold_2, threshold_2], 'r')
plt.plot([time[0], np.max(time[:1000000])], [threshold_3, threshold_3], 'y')

"""""
shifted_frequency = np.roll(frequency, 1)
cycle_time = np.cumsum(period)
plt.figure('Correlation')
color = np.sort(shifted_frequency)
plt.scatter(shifted_frequency, frequency, c=color, marker='.')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Following frequency [Hz]')
plt.axis('equal')


#
# period = 1. / frequencies
# cycle_time = np.cumsum(period)
# plt.figure('Frequency with time')
# plt.plot(cycle_time, frequencies, '.')
# plt.ylabel('Frequency [Hz]')
# plt.xlabel('Time [s]')
# plt.title('Frequency variation in time ')
#
# plt.figure('Histogram')
# plt.hist(frequencies, bins=40)
# plt.xlabel('Frequency [Hz]')
# plt.ylabel('instances')
# plt.title('Histogram of frequencies')
# """""
# plt.figure('Raw data')
# plt.plot(data[::100])
# """""






########
plt.plot(frequency[:-1], frequency[1:], "*")
plt.gca().set_aspect('equal', adjustable='box')
plt.xlim([min(frequency), max(frequency)])
plt.ylim([min(frequency), max(frequency)])