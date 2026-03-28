S2ST v2 — Speech to Speech Translator
======================================

A full pipeline web app that takes your voice, figures out what language
you're speaking, transcribes it, translates it, and plays back the
translation as audio.

Pipeline
--------
Mic → Noise Suppression → VAD → LID → ASR → Translation → TTS


Requirements
------------
Python 3.9 or higher.

Install dependencies:

    pip install -r requirements.txt

You also need ffmpeg installed for pydub audio conversion (fallback path):

    # Ubuntu / Debian
    sudo apt install ffmpeg

    # macOS
    brew install ffmpeg

    # Windows — download from https://ffmpeg.org/download.html


Running the app
---------------
    python app.py

Then open http://localhost:5000 in your browser.

First startup will download the Whisper "base" model (~140 MB).
This only happens once and is cached locally.


How to use
----------
1. Pick source and target languages (or leave source on Auto-detect)
2. Click the red mic button and speak
3. The bar fills up to the max duration, or click the mic again to stop early
4. The app processes the audio through the full pipeline
5. You'll see the original transcription, the translation, and hear the audio
6. Hit Play to replay, Save to get a .txt file, or Share to copy to clipboard


Troubleshooting
---------------
500 error:
  - Check the terminal where you ran app.py — it now logs the full traceback
  - Make sure ffmpeg is installed (needed for non-WAV audio fallback)
  - Make sure all pip dependencies are installed

No voice detected:
  - Speak louder or closer to the mic
  - Check your mic is selected as the default input in your OS settings

Mic access denied in browser:
  - Chrome/Firefox will ask for permission on first use — click Allow
  - If you accidentally denied it, click the lock icon in the address bar


Project structure
-----------------
app.py              Flask web server, /translate endpoint
s2st_app.html       The web UI (single file)
asr.py              Whisper speech recognition
lid.py              Whisper language identification
noise_suppression.py  Bandpass filter for speech frequencies
vad.py              Energy-based voice activity detection
translator.py       Google Translate via deep-translator
tts.py              gTTS text-to-speech (desktop version)
recorder.py         CLI mic recording (desktop version)
main.py             CLI entry point (no browser needed)
requirements.txt    Python dependencies
