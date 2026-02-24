import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# -----------------------
# 1. Load speech
# -----------------------
sampling_rate, signal = wavfile.read("Sample-WAV-File.wav")

# Convert to mono if stereo
if len(signal.shape) > 1:
    signal = signal[:,0]

signal = signal / np.max(np.abs(signal))

# -----------------------
# 2. Frame parameters
# -----------------------
frame_size = int(0.025 * sampling_rate)  # 25 ms
frame_shift = int(0.010 * sampling_rate) # 10 ms

num_frames = int(np.floor((len(signal) - frame_size) / frame_shift)) + 1

# -----------------------
# 3. Pitch detection per frame using autocorrelation
# -----------------------
f0s = []
times = []

energy_threshold = 0.01  # adjust based on signal

for i in range(num_frames):
    start = i * frame_shift
    end = start + frame_size
    frame = signal[start:end]
    
    # Compute frame energy
    energy = np.sum(frame**2) / frame_size
    
    if energy < energy_threshold:
        f0s.append(0)   # unvoiced frame
    else:
        # Autocorrelation
        autocorr = np.correlate(frame, frame, mode='full')
        autocorr = autocorr[frame_size:]  # take positive lags
        
        # Ignore 0 lag and search for peak
        min_lag = int(sampling_rate / 400)  # max F0 ~ 400 Hz
        max_lag = int(sampling_rate / 50)   # min F0 ~ 50 Hz
        
        peak_index = np.argmax(autocorr[min_lag:max_lag]) + min_lag
        pitch = sampling_rate / peak_index
        f0s.append(pitch)
    
    times.append((start + frame_size/2)/sampling_rate)

# -----------------------
# 4. Plot pitch contour
# -----------------------
plt.figure(figsize=(10,4))
plt.plot(times, f0s, '-o', color='blue')
plt.title("Pitch Contour (F0) vs Time")
plt.xlabel("Time (seconds)")
plt.ylabel("Pitch (Hz)")
plt.grid()
plt.show()
