from model import get_model

def get_text(audio, lang=None):
    model = get_model()
    options = {
        "task": "transcribe",
        "beam_size": 5,
        "fp16": False,
    }
    if lang:
        options["language"] = lang
    result = model.transcribe(audio, **options)
    return result["text"].strip()
