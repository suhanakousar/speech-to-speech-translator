import whisper
import soundfile as sf
import tempfile
import os

# load once at startup — lid.py shares the same model object via app.py
# keeping it here simple: one model per module, but we only import this
# module once so it's fine. If RAM is tight, pass the model in from outside.
_model = None

def get_model():
    global _model
    if _model is None:
        _model = whisper.load_model("small")  # higher accuracy than base
    return _model


def get_text(audio, rate, lang=None, lang_conf=None):
    """
    Transcribe audio (float32 numpy array, 16kHz mono) to text.
    lang: ISO 639-1 code or None for auto-detect.
    lang_conf: 0.0-1.0 confidence score from language detection.
    """
    model = get_model()
    tmp = tempfile.mktemp(suffix='.wav')
    sf.write(tmp, audio, rate)
    options = {
        'task': 'transcribe',
        'temperature': 0.0,
        'beam_size': 5,
        'best_of': 5,
    }
    if lang and lang_conf is not None and lang_conf >= 0.65:
        options['language'] = lang
    elif lang and lang_conf is None:
        options['language'] = lang
    # If language detection confidence is low, let Whisper auto-detect.
    result = model.transcribe(tmp, **options)
    os.remove(tmp)
    return result['text'].strip()
