"""
CLI entry point for S2ST — runs the full pipeline from your mic
without the web UI. Useful for quick local testing.

Usage:
    python main.py
"""

from recorder import record
from noise_suppression import clean
from vad import check_voice
from lid import find_language
from asr import get_text
from translator import do_translate
from tts import play


def run():
    duration = 5  # seconds

    
    print(f"Recording {duration}s of audio from your mic...")

    audio, rate = record(duration=duration, rate=16000)
    print("Done recording.")

    audio = clean(audio, rate)
    print("Noise suppression applied.")

    if not check_voice(audio, rate):
        print("No voice detected. Try again in a quieter environment or speak louder.")
        return

    lang, conf = find_language(audio, rate)
    print(f"Detected language: {lang} ({conf:.1%} confidence)")

    if conf < 0.45:
        print("Low language confidence; using auto-detect transcription to reduce errors.")
        text = get_text(audio, rate, lang=None, lang_conf=conf)
    else:
        text = get_text(audio, rate, lang, lang_conf=conf)
    print(f"Transcribed: {text}")

    target = input("Translate to (default: en): ").strip() or 'en'
    translated = do_translate(text, lang, target)
    print(f"Translation: {translated}")

    print("Playing original transcription...")
    play(text, lang)
    print("Playing translated audio...")
    play(translated, target)


if __name__ == '__main__':
    run()
