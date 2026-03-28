import numpy as np

# RMS energy threshold — anything below this is treated as silence.
# 0.005 is a reasonable floor for a 16-bit mic in a quiet room.
THRESHOLD = 0.005


def check_voice(audio, rate):
    """
    Simple energy-based Voice Activity Detection.
    Returns True if audio appears to contain speech, False if it looks like silence.
    """
    if len(audio) == 0:
        return False
    rms = np.sqrt(np.mean(audio.astype(np.float64) ** 2))
    return rms > THRESHOLD
