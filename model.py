import whisper
import threading

_model = None
_lock = threading.Lock()

def get_model():
    global _model
    if _model is not None:
        return _model
    with _lock:
        # Double-check inside the lock in case another thread loaded it first
        if _model is None:
            print("Loading Whisper model...")
            try:
                _model = whisper.load_model("medium")
                print("Whisper medium model loaded!")
            except Exception as e:
                print(f"Could not load medium model ({e}), falling back to small.")
                _model = whisper.load_model("small")
                print("Whisper small model loaded.")
    return _model
