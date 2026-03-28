# S2ST v2 — Speech to Speech Translator

## Overview
A Flask web app that provides a full speech-to-speech translation pipeline:
**Mic → Noise Suppression → VAD → LID → ASR → Translation → TTS**

The user speaks into the microphone, the app detects the language, transcribes the speech using OpenAI Whisper, translates it via Google Translate, and plays back the translation as audio using gTTS.

## Project Structure

| File | Description |
|------|-------------|
| `app.py` | Flask web server with `/` and `/translate` endpoints |
| `s2st_app.html` | Single-file web UI served by Flask |
| `asr.py` | Whisper speech recognition (ASR) |
| `lid.py` | Whisper language identification (LID) |
| `noise_suppression.py` | Bandpass filter for speech frequencies (300–3400 Hz) |
| `vad.py` | Energy-based voice activity detection |
| `translator.py` | Google Translate via deep-translator |
| `tts.py` | gTTS text-to-speech (desktop CLI version) |
| `recorder.py` | CLI mic recording (desktop version) |
| `requirements.txt` | Python dependencies |

## Tech Stack
- **Backend:** Python 3.12, Flask
- **ASR/LID:** OpenAI Whisper (base model, ~140MB, auto-downloaded on first run)
- **Translation:** deep-translator (Google Translate)
- **TTS:** gTTS
- **Audio processing:** numpy, scipy, soundfile, pydub
- **System dependency:** ffmpeg (for audio format fallback)

## Running Locally
The app runs on port 5000 (`0.0.0.0:5000`).

- Development: `python3 app.py`
- Production: `gunicorn --bind=0.0.0.0:5000 --reuse-port app:app`

## Notes
- First startup downloads the Whisper "base" model (~140 MB) — this is cached locally after the first run.
- `asr.py` and `lid.py` were missing from the original repo and were created during Replit setup (they use the openai-whisper library).
- The model is loaded lazily (on first request) and cached in memory for subsequent calls.
