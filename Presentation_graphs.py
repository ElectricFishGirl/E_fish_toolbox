import helpers
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.cm as cmx
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import FormatStrFormatter
from matplotlib import colors
from os.path import join
plt.rcParams.update({'font.size': 30})
matplotlib.rc('xtick', labelsize=28)
matplotlib.rc('ytick', labelsize=28)
fish = 'grinch'

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

numb = 23
index = file_number.index(numb)
file_name = helpers.path_to_name(mat_files[numb])
[frequency, cv, threshold] = helpers.load_npy(npy_files[numb])
period = 1./frequency
m13 = (1./frequency)*1e3
m12 = np.roll(m13, 1)  # shift by one

raw_data = helpers.load_mat(mat_files[numb])
data = np.array(raw_data)
data = data[np.isfinite(data)]
EOD = data - np.mean(data)
time_array = helpers.create_time(len(raw_data)-1, style='MAT')
cycle_time = np.cumsum(1. / frequency)

fig1 = plt.figure('Histogram of ' + file_name)
ax1 = plt.subplot(111)
plt.hist((1./frequency)*1e3, bins=30)
plt.xlabel(' Period [ms]')
plt.ylabel('Occurrences ')
plt.text(1.563, 22.5,  'CV= ' + str(cv), {'color': 'k', 'fontsize': 26})
ax1.xaxis.set_major_formatter(FormatStrFormatter('%.3f'))
plt.locator_params(axis='x', nbins=3)
plt.tight_layout()



fig3 = plt.figure('Period in time' + file_name)
ax2 = plt.subplot(111)
plt.plot(cycle_time, (1./frequency)*1e3, '.', markersize = 12)
plt.ylabel('Period [ms]')
plt.xlabel('Time [s] ')
plt.locator_params(axis='y', nbins=3)
ax2.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
plt.tight_layout()

fig4 = plt.figure('Autocorrelation' + file_name)
period = (1./frequency)*1e3
plt.acorr(period-period.mean(), usevlines=True, maxlags=10, normed=True, lw=4)
plt.grid(True)
plt.axhline(0, color='black', lw=4)
plt.xlabel('Lag [cycles]')
plt.ylabel('Autocorrelation')
plt.tight_layout()

fig2 = plt.figure('Return Map ' + file_name)
cm = plt.cm.get_cmap('viridis')
ax1 = fig2.add_subplot(221)
m13 = (1./frequency)*1e3
m12 = np.roll(m13, 1)  # shift by one
sc = ax1.scatter(m13, m12, c=range(0, len(m12)), cmap=cm)
plt.locator_params(axis='y', nbins=3)
cbar_ax = plt.colorbar(sc)
cbar_ax.set_ticks([0, len(m13)-1])
cbar_ax.set_ticklabels(['Start', 'End'])
ax1.set_xlabel('$T_i$ [ms]')
ax1.set_ylabel('$T_{i+1}$ [ms]')
ax1.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
ax1.xaxis.set_major_formatter(FormatStrFormatter('%.3f'))
data_min, data_max = np.min(np.concatenate((m13, m12))), np.max(np.concatenate((m13, m12)))
rng = data_max-data_min
plt.xlim(data_min-0.1*rng, data_max+0.1*rng)
plt.ylim(data_min-0.1*rng, data_max+0.1*rng)
ax1.set_aspect('equal', 'box')



plt.rcParams.update({'font.size': 25})
matplotlib.rc('xtick', labelsize=22)
matplotlib.rc('ytick', labelsize=22)
fig = plt.figure('Drugs' + file_name)
cm = plt.cm.get_cmap('viridis')
ax1 = fig.add_subplot(221)
m13 = (1./frequency)*1e3
m12 = np.roll(m13, 1)  # shift by one
sc = ax1.scatter(m13, m12, c=range(0, len(m12)), cmap=cm)
cbar_ax = plt.colorbar(sc)
plt.locator_params(axis='y', nbins=2)
plt.locator_params(axis='x', nbins=2)
cbar_ax.set_ticks([0, len(m13)-1])
cbar_ax.set_ticklabels(['Start', 'End'])
ax1.set_xlabel('$T_i$ [ms]')
ax1.set_ylabel('$T_{i+1}$ [ms]')
ax1.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
ax1.xaxis.set_major_formatter(FormatStrFormatter('%.3f'))
data_min, data_max = np.min(np.concatenate((m13, m12))), np.max(np.concatenate((m13, m12)))
rng = data_max-data_min
plt.xlim(data_min-0.1*rng, data_max+0.1*rng)
plt.ylim(data_min-0.1*rng, data_max+0.1*rng)
ax1.set_aspect('equal')

ax2 = fig.add_subplot(222)
period = (1./frequency)*1e3
ax2.acorr(period-period.mean(), usevlines=True, maxlags=10, normed=True, lw=4)
ax2.grid(True)
ax2.text(-1, 1.2,  'Dose 4 ; CV = '+ str(cv), {'color': 'k', 'fontsize': 26})
ax2.axhline(0, color='black', lw=4)
ax2.set_xlabel('Lag [cycles]')
ax2.set_ylabel('Autocorrelation')
