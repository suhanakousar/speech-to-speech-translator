import whisper

_model = None

def get_model():
    global _model
    if _model is None:
        print("Loading Whisper model...")
        _model = whisper.load_model("medium")
        print("Model loaded!")
    return _model
