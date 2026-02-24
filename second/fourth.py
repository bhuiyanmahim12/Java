import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fftpack import dct

# ------------------------
# 1. Load Audio
# ------------------------
sampling_rate, signal = wavfile.read("Sample-WAV-File.wav")

# Convert to mono if stereo
if len(signal.shape) > 1:
    signal = signal[:, 0]

# Normalize signal
signal = signal / np.max(np.abs(signal))

# ------------------------
# 2. Pre-emphasis
# ------------------------
pre_emphasis = 0.97
emphasized_signal = np.append(signal[0], signal[1:] - pre_emphasis * signal[:-1])

# ------------------------
# 3. Framing
# ------------------------
frame_size = 0.025  # 25 ms
frame_shift = 0.010 # 10 ms

frame_length = int(frame_size * sampling_rate)
frame_step = int(frame_shift * sampling_rate)
signal_length = len(emphasized_signal)
num_frames = int(np.ceil(float(np.abs(signal_length - frame_length)) / frame_step)) + 1

pad_signal_length = num_frames * frame_step + frame_length
z = np.zeros((pad_signal_length - signal_length))
pad_signal = np.append(emphasized_signal, z)

indices = np.tile(np.arange(0, frame_length), (num_frames,1)) + np.tile(np.arange(0, num_frames*frame_step, frame_step), (frame_length,1)).T
frames = pad_signal[indices.astype(np.int32, copy=False)]

# Apply Hamming window
frames *= np.hamming(frame_length)

# ------------------------
# 4. FFT and Power Spectrum
# ------------------------
NFFT = 512
mag_frames = np.absolute(np.fft.rfft(frames, NFFT))
pow_frames = ((1.0 / NFFT) * (mag_frames ** 2))

# ------------------------
# 5. Mel Filterbank
# ------------------------
nfilt = 26
low_freq_mel = 0
high_freq_mel = 2595 * np.log10(1 + (sampling_rate/2)/700)
mel_points = np.linspace(low_freq_mel, high_freq_mel, nfilt + 2)
hz_points = 700 * (10**(mel_points/2595) - 1)
bin = np.floor((NFFT + 1) * hz_points / sampling_rate)

fbank = np.zeros((nfilt, int(NFFT/2 + 1)))
for m in range(1, nfilt+1):
    f_m_minus = int(bin[m-1])
    f_m = int(bin[m])
    f_m_plus = int(bin[m+1])
    
    for k in range(f_m_minus, f_m):
        fbank[m-1,k] = (k - bin[m-1]) / (bin[m] - bin[m-1])
    for k in range(f_m, f_m_plus):
        fbank[m-1,k] = (bin[m+1] - k) / (bin[m+1] - bin[m])

filter_banks = np.dot(pow_frames, fbank.T)
filter_banks = np.where(filter_banks == 0, np.finfo(float).eps, filter_banks)
filter_banks = 20 * np.log10(filter_banks)

# ------------------------
# 6. DCT to get MFCC
# ------------------------
num_ceps = 13
mfcc = dct(filter_banks, type=2, axis=1, norm='ortho')[:, :num_ceps]

# ------------------------
# 7. Plot MFCC Heatmap
# ------------------------
plt.figure(figsize=(10,5))
plt.imshow(mfcc.T, aspect='auto', origin='lower', cmap='jet')
plt.title("MFCC Heatmap")
plt.xlabel("Frame Index")
plt.ylabel("MFCC Coefficient Index")
plt.colorbar(label="Amplitude (dB)")
plt.show()
