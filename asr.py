from model import get_model

def get_text(audio, lang=None):
    model = get_model()
    if lang:
        result = model.transcribe(audio, language=lang)
    else:
        result = model.transcribe(audio)
    return result["text"].strip()
