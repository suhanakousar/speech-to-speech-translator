import sounddevice as sd
import soundfile as sf
import numpy as np


def record(duration=5, rate=16000):
    """
    Record audio from the default mic for `duration` seconds.
    Returns float32 numpy array at the given sample rate.
    This is the CLI/desktop version. The web app records in the browser.
    """
    print(f"Recording for {duration}s...")
    audio = sd.rec(int(duration * rate), samplerate=rate, channels=1, dtype='float32')
    sd.wait()
    return audio.flatten(), rate
