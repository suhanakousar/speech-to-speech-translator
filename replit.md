# S2ST v2 — Speech to Speech Translator

## Overview
A full-pipeline web application that performs real-time speech translation:
Mic → Noise Suppression → VAD → Language ID → ASR (Whisper) → Translation → TTS → Playback

## Architecture
- **Backend**: Python/Flask, runs on port 5000 (0.0.0.0)
- **Frontend**: Single HTML file (`s2st_app.html`) served by Flask at `/`
- **Entry point**: `app.py`

## Key Technologies
- **Flask** — web server and API
- **OpenAI Whisper** — speech recognition and language identification
- **deep-translator** — Google Translate integration
- **gTTS** — Google Text-to-Speech
- **NumPy/SciPy** — audio signal processing
- **PyDub + FFmpeg** — audio format conversion (WebM/OGG → WAV)
- **SoundFile** — audio I/O

## Project Layout
```
app.py              # Flask entry point, /translate API endpoint
s2st_app.html       # Single-file frontend (HTML/CSS/JS)
asr.py              # Speech-to-Text via Whisper
lid.py              # Language Identification via Whisper
translator.py       # Translation wrapper (deep-translator)
tts.py              # Text-to-Speech (gTTS)
noise_suppression.py # Bandpass filter for audio cleanup
vad.py              # Voice Activity Detection
model.py            # Whisper model loader
recorder.py         # CLI microphone recording utility
requirements.txt    # Python dependencies
```

## Running the App
The workflow runs: `python app.py`
The app listens on `0.0.0.0:5000`.

## Deployment
Configured for autoscale deployment using:
`gunicorn --bind=0.0.0.0:5000 --reuse-port app:app`

## System Dependencies
- `ffmpeg` — required for audio format conversion via PyDub
