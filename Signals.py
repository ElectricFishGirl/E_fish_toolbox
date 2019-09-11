import numpy as np
import matplotlib.pyplot as plt
from lewisfunctions.frequency import calculate_frequency

sampling_frequency = 41666.666666
time = np.arange(0, 3, 1/sampling_frequency)
f = 900
One_sin = np.sin(2*np.pi*f*time)
#plt.figure('one_sin')
#plt.plot(time, One_sin)
Two_sin = 4*np.sin(2*np.pi*f*time) + 2*np.sin(2*np.pi*f*2*time)
#plt.figure('Two_sin')
#plt.plot(time, Two_sin)
noise = np.random.normal(0, 1, len(time))

noisy = 255*One_sin + 0.01*noise
plt.plot(noisy)
fest = calculate_frequency(noisy[::20], fs=sampling_frequency/20, method='spectral')
measured = calculate_frequency(noisy, temporal_threshold=0.05, fs=sampling_frequency, crossing_threshold= 4, ascending=False, estimated_frequency=fest[0], method='simple')

frequency = measured
plt.plot(frequency[:-1], frequency[1:], "*")
plt.gca().set_aspect('equal', adjustable='box')
plt.xlim([min(frequency), max(frequency)])
plt.ylim([min(frequency), max(frequency)])
# plt.plot('Correlation')
# plt.acorr(frequency, usevlines=True, maxlags=50, normed=True, lw=2)
# plt.grid(True)
# plt.axhline(0, color='black', lw=2)
# plt.title('Correlation')


from scipy.signal import hilbert
signal = noisy[1:20833333]
analytic_signal = hilbert(signal)  # instead of EODs
amplitude_envelope = np.abs(analytic_signal)
instantaneous_phase = np.unwrap(np.angle(analytic_signal)) / (2.0 * np.pi)
instant_mod = np.mod(instantaneous_phase, 1)
instantaneous_frequency = np.diff(instantaneous_phase) * sampling_frequency
aveg_freq_H = np.mean(instantaneous_frequency)
instant_mod = instant_mod - np.mean(instant_mod)
instant_mod = instant_mod / np.std(instant_mod)
thresh2 = 1.2 * np.std(instant_mod)
instant_mod2 = np.roll(instant_mod, -1)
cyclei3 = np.array(np.where((instant_mod < thresh2) & (instant_mod2 > thresh2))).T
instant_mod_cross = time[cyclei3[1:len(cyclei3) - 1]]
instant_mod_period = np.diff(instant_mod_cross, axis=0)
instant_mod_freq = 1. / instant_mod_period
