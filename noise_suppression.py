import numpy as np
from scipy.signal import butter, sosfilt

def clean(audio, rate):
    nyq = rate / 2.0
    low = 300.0 / nyq
    high = 3400.0 / nyq

    low = max(low, 0.001)
    high = min(high, 0.999)

    if low >= high:
        return audio

    sos = butter(4, [low, high], btype='bandpass', output='sos')
    filtered = sosfilt(sos, audio)
    return filtered.astype(np.float32)
