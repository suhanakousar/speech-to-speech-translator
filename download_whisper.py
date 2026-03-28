"""
Run during deploy build to cache the Whisper weights (avoids downloading on first HTTP request).

Render: add to Build Command, after pip install:
  python download_whisper.py

Set WHISPER_MODEL in the dashboard (e.g. base) for both build and runtime — same as `model.requested_model_name()`.
"""
import whisper
from model import requested_model_name

name = requested_model_name()
print(f"Downloading Whisper model for build cache: {name}")
whisper.load_model(name)
print("Whisper model cached OK.")
