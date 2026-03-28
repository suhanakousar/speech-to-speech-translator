import numpy as np

def has_voice(audio):
    if len(audio) == 0:
        return False
    rms = np.sqrt(np.mean(audio.astype(np.float64) ** 2))
    return rms > 0.005
