import os
import whisper
import threading

_model = None
_lock = threading.Lock()


def requested_model_name():
    """Same default for runtime and `download_whisper.py` build step."""
    return (os.environ.get("WHISPER_MODEL") or "medium").strip() or "medium"


def _model_candidates():
    """Prefer WHISPER_MODEL (default: medium); fall back to smaller models if load fails."""
    preferred = requested_model_name()
    order = [preferred]
    for fb in ("small", "base", "tiny"):
        if fb not in order:
            order.append(fb)
    return order


def get_model():
    global _model
    if _model is not None:
        return _model
    with _lock:
        if _model is None:
            last_err = None
            for name in _model_candidates():
                try:
                    print(f"Loading Whisper model: {name}...")
                    _model = whisper.load_model(name)
                    print(f"Whisper model ready ({name}).")
                    break
                except Exception as e:
                    last_err = e
                    print(f"Could not load {name}: {e}")
            if _model is None:
                raise RuntimeError(f"No Whisper model could be loaded: {last_err}")
    return _model
