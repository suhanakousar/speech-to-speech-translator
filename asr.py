import whisper
import numpy as np

_model = None


def _get_model():
    global _model
    if _model is None:
        _model = whisper.load_model("base")
    return _model


def get_text(audio, rate, lang=None):
    """
    Transcribe audio using OpenAI Whisper.
    audio: float32 numpy array at 16 kHz
    lang: ISO 639-1 language code or None for auto-detect
    Returns transcribed string.
    """
    model = _get_model()
    audio = audio.astype(np.float32)

    options = {}
    if lang:
        options["language"] = lang

    result = model.transcribe(audio, **options)
    return result.get("text", "").strip()
