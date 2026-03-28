from model import get_model

def get_text(audio, lang=None):
    model = get_model()
    options = {
        "task": "transcribe",
        "beam_size": 5,
        "fp16": False,
        "condition_on_previous_text": False,
        "no_speech_threshold": 0.4,
        "logprob_threshold": -1.0,
    }
    if lang:
        options["language"] = lang
    result = model.transcribe(audio, **options)
    return result["text"].strip()
