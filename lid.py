import whisper
import numpy as np

_model = None


def _get_model():
    global _model
    if _model is None:
        _model = whisper.load_model("base")
    return _model


def find_language(audio, rate):
    """
    Detect the language of the audio using Whisper's language identification.
    audio: float32 numpy array at 16 kHz
    Returns (language_code, confidence) where language_code is ISO 639-1.
    """
    model = _get_model()
    audio = audio.astype(np.float32)

    audio_padded = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio_padded).to(model.device)

    _, probs = model.detect_language(mel)
    lang = max(probs, key=probs.get)
    confidence = probs[lang]
    return lang, confidence
