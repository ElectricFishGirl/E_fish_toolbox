import helpers
import numpy as np
import matplotlib.pyplot as plt
from os.path import join

fish = 'Moush'

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

numb = 7
index = file_number.index(numb)
raw_data = helpers.load_mat(mat_files[numb])
data = np.array(raw_data)
data = data[np.isfinite(data)]
EOD = data - np.mean(data)
file_name = helpers.path_to_name(mat_files[numb])
[frequency, cv, threshold] = helpers.load_npy(npy_files[numb])
period = 1./frequency
time_array = helpers.create_time(len(raw_data)-1, style='MAT')
cycle_time = np.cumsum(1. / frequency)


fig = plt.figure('Drugs' + file_name)
ax1 = fig.add_subplot(222)
ax1.hist((1./frequency)*1e3, bins = 20)
ax1.set_title('Histogram of periods ;  ' + ' CV = ' + str(cv))
ax1.set_xlabel(' period [ms]')
ax1.set_ylabel('Occurrences ')

ax2 = fig.add_subplot(221)
period = (1./frequency)*1e3
ax2.acorr(period-period.mean(), usevlines=True, maxlags=10, normed=True, lw=2)
ax2.grid(True)
ax2.axhline(0, color='black', lw=2)
ax2.set_title('Dose 4 ; Auto-Correlation')

fig = plt.figure('Histogram of ' + file_name)
plt.hist((1./frequency)*1e3, bins = 20)
plt.title('Histogram of periods ;  ' + ' CV = ' + str(cv))
plt.xlabel(' period [ms]')
plt.ylabel('Occurrences ')

fig2 = plt.figure('Shifted frequency' + file_name)
m13 = (1./frequency)*1e3
m12 = np.roll(m13, 1)  # shift by one
color = np.sort(m13)
plt.scatter(m13, m12, c=color, marker='.')
plt.title('Shifted period [ms]')
plt.axis('equal')


fig4 = plt.figure('Period in time' + file_name)
plt.plot(cycle_time, (1./frequency)*1e3, '.')
plt.title('Period with time')
plt.ylabel('Period [ms]')
plt.xlabel('Time [s] ')
fig5 = plt.figure('Autocorrelation' + file_name)
period = (1./frequency)*1e3
plt.acorr(period-period.mean(), usevlines=True, maxlags=10, normed=True, lw=2)
plt.grid(True)
plt.axhline(0, color='black', lw=2)
plt.title('Auto-Correlation')


