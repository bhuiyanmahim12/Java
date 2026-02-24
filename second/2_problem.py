import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# -----------------------------
# 1. Load speech file
# -----------------------------
sampling_rate, signal = wavfile.read("Sample-WAV-File.wav")

# Convert to mono if stereo
if len(signal.shape) > 1:
    signal = signal[:, 0]

# -----------------------------
# 2. Define frame parameters
# -----------------------------
frame_size_ms = 25
frame_shift_ms = 10

frame_size = int(sampling_rate * frame_size_ms / 1000)
frame_shift = int(sampling_rate * frame_shift_ms / 1000)

signal_length = len(signal)

# -----------------------------
# 3. Calculate total frames
# -----------------------------
num_frames = int(np.floor((signal_length - frame_size) / frame_shift)) + 1

print("Frame Size (samples):", frame_size)
print("Frame Shift (samples):", frame_shift)
print("Total Number of Frames:", num_frames)

# -----------------------------
# 4. Create frames (from scratch)
# -----------------------------
frames = []

for i in range(num_frames):
    start = i * frame_shift
    end = start + frame_size
    frame = signal[start:end]
    frames.append(frame)

frames = np.array(frames)

# -----------------------------
# 5. Apply Hamming window
# -----------------------------
hamming_window = 0.54 - 0.46 * np.cos(
    2 * np.pi * np.arange(frame_size) / (frame_size - 1)
)

windowed_frames = frames * hamming_window

# -----------------------------
# 6. Plot one sample frame
# -----------------------------
sample_index = 5   # choose any frame

plt.figure()
plt.plot(frames[sample_index])
plt.title("Original Frame")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.grid()
plt.show()

plt.figure()
plt.plot(windowed_frames[sample_index])
plt.title("Windowed Frame (Hamming Applied)")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.grid()
plt.show()
