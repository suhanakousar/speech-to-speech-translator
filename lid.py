import whisper
from model import get_model

def find_language(audio):
    model = get_model()
    audio_clipped = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio_clipped).to(model.device)
    _, probs = model.detect_language(mel)
    best_lang = max(probs, key=probs.get)
    return best_lang, probs[best_lang]
