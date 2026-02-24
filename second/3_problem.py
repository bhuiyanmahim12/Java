import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# -------------------------
# 1. Load the audio
# -------------------------
sampling_rate, signal = wavfile.read("Sample-WAV-File.wav")

# Convert stereo to mono if needed
if len(signal.shape) > 1:
    signal = signal[:, 0]

# Normalize the signal
signal = signal / np.max(np.abs(signal))

# -------------------------
# 2. Frame parameters
# -------------------------
frame_size_ms = 25  # 25 ms
frame_shift_ms = 10 # 10 ms

frame_size = int(sampling_rate * frame_size_ms / 1000)
frame_shift = int(sampling_rate * frame_shift_ms / 1000)

num_frames = int(np.floor((len(signal) - frame_size) / frame_shift)) + 1
print("Frame size (samples):", frame_size)
print("Frame shift (samples):", frame_shift)
print("Total number of frames:", num_frames)

# Hamming window
hamming_window = np.hamming(frame_size)

# -------------------------
# 3. Compute STFT using rFFT
# -------------------------
stft_matrix = []

for i in range(num_frames):
    start = i * frame_shift
    end = start + frame_size
    frame = signal[start:end]
    
    windowed_frame = frame * hamming_window
    
    spectrum = np.fft.rfft(windowed_frame)  # Real FFT
    stft_matrix.append(np.abs(spectrum))

# Convert to numpy array
stft_matrix = np.array(stft_matrix).T  # transpose to freq x time

# -------------------------
# 4. Convert magnitude to dB
# -------------------------
spectrogram_db = 20 * np.log10(stft_matrix + 1e-8)  # avoid log(0)

# -------------------------
# 5. Plot Spectrogram
# -------------------------
plt.figure(figsize=(10,5))
plt.imshow(spectrogram_db, 
           aspect='auto', 
           origin='lower',
           extent=[0, len(signal)/sampling_rate, 0, sampling_rate/2],
           cmap='jet')

plt.colorbar(label='Magnitude (dB)')
plt.title("Spectrogram of Speech Signal")
plt.xlabel("Time (seconds)")
plt.ylabel("Frequency (Hz)")
plt.show()
