import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# -------------------------------
# 1. Load the audio file
# -------------------------------
file_path = "Sample-WAV-File.wav"   # Replace with your file name

sampling_rate, signal = wavfile.read(file_path)

# If stereo, convert to mono
if len(signal.shape) > 1:
    signal = signal[:, 0]

# -------------------------------
# 2. Basic Information
# -------------------------------
num_samples = len(signal)
duration = num_samples / sampling_rate
max_amplitude = np.max(signal)
min_amplitude = np.min(signal)

print("Sampling Rate:", sampling_rate, "Hz")
print("Number of Samples:", num_samples)
print("Duration:", duration, "seconds")
print("Maximum Amplitude:", max_amplitude)
print("Minimum Amplitude:", min_amplitude)

# -------------------------------
# 3. Plot Waveform
# -------------------------------
time_axis = np.linspace(0, duration, num_samples)

plt.figure()
plt.plot(time_axis, signal)
plt.title("Waveform of Speech Signal")
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.grid()
plt.show() 

# -------------------------------
# 4. FFT (Frequency Spectrum)
# -------------------------------
fft_values = np.fft.fft(signal)
fft_magnitude = np.abs(fft_values)

freq_axis = np.fft.fftfreq(num_samples, 1/sampling_rate)

# Take only positive frequencies
positive_freqs = freq_axis[:num_samples // 2]
positive_magnitude = fft_magnitude[:num_samples // 2]

plt.figure()
plt.plot(positive_freqs, positive_magnitude)
plt.title("Magnitude Spectrum")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.grid()
plt.show()
