import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import stft, istft

# -----------------------------
# 1. Load WAV File
# -----------------------------
sr, speech = wavfile.read("Sample-WAV-File.wav")

# যদি stereo হয় → mono করবো
if len(speech.shape) == 2:
    speech = speech[:, 0]

# Normalize
speech = speech.astype(np.float64)
speech = speech / np.max(np.abs(speech))

# -----------------------------
# 2. Add White Noise (10 dB SNR)
# -----------------------------
def add_noise(signal, snr_db):
    signal_power = np.mean(signal**2)
    snr_linear = 10**(snr_db/10)
    noise_power = signal_power / snr_linear
    
    noise = np.random.normal(0, np.sqrt(noise_power), signal.shape)
    noisy_signal = signal + noise
    return noisy_signal, noise

noisy_speech, noise = add_noise(speech, 10)

# -----------------------------
# 3. Compute SNR
# -----------------------------
def compute_snr(clean, noisy):
    noise = noisy - clean
    return 10 * np.log10(np.sum(clean**2) / np.sum(noise**2))

snr_before = compute_snr(speech, noisy_speech)
print("SNR Before Enhancement: %.2f dB" % snr_before)

# -----------------------------
# 4. Spectral Subtraction
# -----------------------------
n_fft = 1024
hop = 512

f, t, Zxx = stft(noisy_speech, fs=sr, nperseg=n_fft, noverlap=n_fft-hop)

magnitude = np.abs(Zxx)
phase = np.angle(Zxx)

# First 5 frames assumed noise-only
noise_mag = np.mean(magnitude[:, :5], axis=1, keepdims=True)

# Spectral subtraction
enhanced_mag = magnitude - noise_mag
enhanced_mag = np.maximum(enhanced_mag, 0.001)

# Reconstruct
Zxx_enhanced = enhanced_mag * np.exp(1j * phase)
_, enhanced_speech = istft(Zxx_enhanced, fs=sr, nperseg=n_fft, noverlap=n_fft-hop)

# -----------------------------
# 5. Compute SNR After
# -----------------------------
min_len = min(len(speech), len(enhanced_speech))
snr_after = compute_snr(speech[:min_len], enhanced_speech[:min_len])

print("SNR After Enhancement: %.2f dB" % snr_after)
print("SNR Improvement: %.2f dB" % (snr_after - snr_before))

# -----------------------------
# 6. Plot Signals
# -----------------------------
plt.figure(figsize=(12,8))

plt.subplot(3,1,1)
plt.title("Original Speech")
plt.plot(speech)

plt.subplot(3,1,2)
plt.title("Noisy Speech (10 dB)")
plt.plot(noisy_speech)

plt.subplot(3,1,3)
plt.title("Enhanced Speech (Spectral Subtraction)")
plt.plot(enhanced_speech)

plt.tight_layout()
plt.show()
