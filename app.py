from flask import Flask, request, jsonify, render_template_string
import numpy as np
import soundfile as sf
import io
import tempfile
import os
import base64
import traceback
import logging

from noise_suppression import clean
from vad import check_voice
from lid import find_language
from asr import get_text
from translator import do_translate

# set up basic logging so errors actually show up in the terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

app = Flask(__name__)

# language codes that Whisper gives back vs what gTTS expects
# Whisper uses ISO 639-1, gTTS is mostly the same but a few edge cases
GTTS_LANG_MAP = {
    'zh': 'zh-CN',
    'jw': 'jv',   # Javanese
    'sr': 'sr',
    'af': 'af',
}

def normalize_lang(code):
    """Map Whisper language codes to gTTS-compatible codes."""
    return GTTS_LANG_MAP.get(code, code)


def read_audio_bytes(audio_bytes):
    """
    Try to read audio bytes into a numpy float32 array.
    Handles WAV (what the frontend sends) and falls back to
    pydub for anything else (webm, ogg, mp4 etc).
    Returns (audio_array, sample_rate).
    """
    # first try soundfile directly — works great for WAV
    try:
        buf = io.BytesIO(audio_bytes)
        audio, rate = sf.read(buf, dtype='float32')
        return audio, rate
    except Exception:
        pass

    # fallback: pydub can handle webm / ogg / mp4 that MediaRecorder sometimes sends
    try:
        from pydub import AudioSegment
        tmp_in = tempfile.mktemp(suffix='.audio')
        tmp_wav = tempfile.mktemp(suffix='.wav')
        with open(tmp_in, 'wb') as f:
            f.write(audio_bytes)
        seg = AudioSegment.from_file(tmp_in)
        seg = seg.set_frame_rate(16000).set_channels(1)
        seg.export(tmp_wav, format='wav')
        os.remove(tmp_in)
        audio, rate = sf.read(tmp_wav, dtype='float32')
        os.remove(tmp_wav)
        return audio, rate
    except Exception as e:
        raise ValueError(f"Could not decode audio: {e}")


def generate_tts(text, lang):
    """Run gTTS and return the mp3 as base64."""
    from gtts import gTTS
    gtts_lang = normalize_lang(lang)
    tmp = tempfile.mktemp(suffix='.mp3')
    try:
        tts = gTTS(text=text, lang=gtts_lang, slow=False)
        tts.save(tmp)
        if not os.path.exists(tmp):
            raise FileNotFoundError(f"gTTS failed to create MP3 file: {tmp}")
        with open(tmp, 'rb') as f:
            data = f.read()
        if len(data) == 0:
            raise ValueError("gTTS generated empty MP3 file")
        log.info(f"Generated TTS audio: {len(data)} bytes from {len(text)} chars")
        os.remove(tmp)
        return base64.b64encode(data).decode('utf-8')
    except Exception as e:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise ValueError(f"TTS generation failed: {e}")


@app.route('/')
def index():
    html_path = os.path.join(os.path.dirname(__file__), 's2st_app.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    return render_template_string(html)


@app.route('/translate', methods=['POST'])
def translate():
    try:
        # ── 1. pull audio out of the request ──────────────────────────────
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file attached to request'}), 400

        audio_bytes = request.files['audio'].read()
        if not audio_bytes:
            return jsonify({'error': 'Audio file is empty'}), 400

        log.info(f"Received audio: {len(audio_bytes)} bytes")

        # ── 2. decode to float32 numpy array ──────────────────────────────
        audio, rate = read_audio_bytes(audio_bytes)
        log.info(f"Decoded audio: shape={audio.shape}, rate={rate}")

        # make mono
        if audio.ndim > 1:
            audio = audio.mean(axis=1)

        # resample to 16 kHz if needed (Whisper expects 16k)
        if rate != 16000:
            import scipy.signal as sig
            num_samples = int(len(audio) * 16000 / rate)
            audio = sig.resample(audio, num_samples).astype(np.float32)
            rate = 16000

        # ── 3. noise suppression ──────────────────────────────────────────
        audio = clean(audio, rate)

        # ── 4. VAD — make sure someone actually spoke ─────────────────────
        if not check_voice(audio, rate):
            return jsonify({'error': 'No voice detected in the recording. Try speaking louder or closer to the mic.'}), 400

        # ── 5. language identification ────────────────────────────────────
        src_lang, confidence = find_language(audio, rate)
        log.info(f"LID: {src_lang} ({confidence:.2%})")

        # ── 6. ASR ────────────────────────────────────────────────────────
        text = get_text(audio, rate, src_lang)
        log.info(f"ASR: {text!r}")

        if not text.strip():
            return jsonify({'error': 'Could not transcribe any speech. Please try again.'}), 400

        # ── 7. translation ────────────────────────────────────────────────
        tgt_lang = request.form.get('target_lang', 'en').strip()
        translated = do_translate(text, src_lang, tgt_lang)
        log.info(f"Translated: {translated!r}")

        # ── 8. TTS ────────────────────────────────────────────────────────
        log.info(f"Starting TTS generation for language: {tgt_lang}")
        audio_b64 = generate_tts(translated, tgt_lang)
        log.info(f"TTS complete, generated {len(audio_b64)} chars of base64")

        return jsonify({
            'original_text': text,
            'translated_text': translated,
            'src_lang': src_lang,
            'tgt_lang': tgt_lang,
            'confidence': float(confidence),
            'audio_b64': audio_b64,
        })

    except Exception as e:
        log.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
