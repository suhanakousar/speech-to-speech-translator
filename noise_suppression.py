import numpy as np
from scipy.signal import butter, sosfilt


def clean(audio, rate):
    """
    Apply a bandpass filter to keep the speech frequency range (300–3400 Hz).
    Uses second-order sections (sosfilt) which is more numerically stable
    than the original lfilter approach, especially at low sample rates.
    Returns float32 array.
    """
    audio = audio.astype(np.float32)
    nyq = rate / 2.0
    low = 300.0 / nyq
    high = 3400.0 / nyq

    # clamp to valid range just in case of an unusual sample rate
    low = max(low, 0.001)
    high = min(high, 0.999)

    if low >= high:
        # can't filter, return as-is
        return audio

    sos = butter(4, [low, high], btype='bandpass', output='sos')
    filtered = sosfilt(sos, audio)
    return filtered.astype(np.float32)
