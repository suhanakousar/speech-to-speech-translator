import numpy as np
from scipy.signal import butter, sosfilt

def clean(audio, rate):
    nyq = rate / 2.0
    # Wider band (80–8000 Hz) captures full speech range without over-filtering
    low = 80.0 / nyq
    high = min(8000.0 / nyq, 0.999)

    low = max(low, 0.001)

    if low >= high:
        return audio

    # Lower filter order (2) for a gentler roll-off — less speech distortion
    sos = butter(2, [low, high], btype='bandpass', output='sos')
    filtered = sosfilt(sos, audio)
    return filtered.astype(np.float32)
