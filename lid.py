import whisper
import numpy as np

_model = None

def get_model():
    global _model
    if _model is None:
        _model = whisper.load_model("small")  # higher accuracy than base
    return _model


def find_language(audio, rate):
    """
    Detect the spoken language in audio (float32 numpy, 16kHz mono).
    Returns (language_code, confidence_float).
    """
    model = get_model()
    # whisper.pad_or_trim expects float32
    trimmed = whisper.pad_or_trim(audio.astype(np.float32))
    mel = whisper.log_mel_spectrogram(trimmed).to(model.device)
    _, probs = model.detect_language(mel)
    best = max(probs, key=probs.get)
    return best, float(probs[best])
