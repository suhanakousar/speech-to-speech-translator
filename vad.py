import numpy as np

def has_voice(audio):
    if len(audio) == 0:
        return False
    # Normalize to check relative energy, not absolute level
    peak = np.max(np.abs(audio))
    if peak < 1e-7:
        return False
    normalized = audio / peak
    rms = np.sqrt(np.mean(normalized.astype(np.float64) ** 2))
    # Lower threshold — catches quieter speech after normalization
    return rms > 0.02
