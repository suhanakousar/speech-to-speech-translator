from flask import Flask, request, jsonify
import numpy as np
import soundfile as sf
import scipy.signal as sig
import io
import tempfile
import os
import base64

from noise_suppression import clean
from vad import has_voice
from lid import find_language
from asr import get_text
from translator import do_translate

app = Flask(__name__)

# some languages have different codes between Whisper and gTTS
LANG_FIX = {
    'zh': 'zh-CN',
    'jw': 'jv',
}

def fix_lang(code):
    return LANG_FIX.get(code, code)

def load_audio(audio_bytes):
    # try reading directly as WAV first
    try:
        buf = io.BytesIO(audio_bytes)
        audio, rate = sf.read(buf, dtype='float32')
        return audio, rate
    except Exception:
        pass

    # fallback for webm/ogg using pydub
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

def make_tts(text, lang):
    from gtts import gTTS
    tmp = tempfile.mktemp(suffix='.mp3')
    tts = gTTS(text=text, lang=fix_lang(lang), slow=False)
    tts.save(tmp)
    with open(tmp, 'rb') as f:
        data = f.read()
    os.remove(tmp)
    return base64.b64encode(data).decode('utf-8')

@app.route('/')
def index():
    with open('s2st_app.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/translate', methods=['POST'])
def translate():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file in request'}), 400

        audio_bytes = request.files['audio'].read()
        if not audio_bytes:
            return jsonify({'error': 'Audio file is empty'}), 400

        # decode audio to numpy array
        audio, rate = load_audio(audio_bytes)

        # make mono
        if audio.ndim > 1:
            audio = audio.mean(axis=1)

        # resample to 16kHz if needed
        if rate != 16000:
            n = int(len(audio) * 16000 / rate)
            audio = sig.resample(audio, n).astype(np.float32)
            rate = 16000

        # Normalize audio level to a consistent peak so VAD and ASR
        # work reliably regardless of mic volume or upload loudness
        peak = np.max(np.abs(audio))
        if peak > 1e-7:
            audio = audio / peak * 0.9

        # apply noise filter only for mic recordings — uploaded files are
        # usually already good quality and the filter can hurt accuracy
        is_upload = request.form.get('is_upload', 'false') == 'true'
        if not is_upload:
            audio = clean(audio, rate)

        # check that someone actually spoke
        if not has_voice(audio):
            return jsonify({'error': 'No voice detected. Try speaking louder.'}), 400

        # use user-selected source language if given, otherwise auto-detect
        selected_src = request.form.get('src_lang', 'auto').strip()
        if selected_src and selected_src != 'auto':
            src_lang = selected_src
            confidence = 1.0
            print(f"Source language set by user: {src_lang}")
        else:
            src_lang, confidence = find_language(audio)
            print(f"Detected language: {src_lang} ({confidence:.0%})")

        # transcribe — pass the language so Whisper uses the right one
        text = get_text(audio, src_lang)
        print(f"Transcribed: {text!r}")

        if not text:
            return jsonify({'error': 'Could not transcribe speech. Please try again.'}), 400

        # translate — use 'auto' as source so Google Translate detects the
        # actual script of the transcribed text (Whisper sometimes outputs
        # a different script than expected, e.g. Devanagari for Telugu)
        tgt_lang = request.form.get('target_lang', 'en').strip()
        translated = do_translate(text, 'auto', tgt_lang)
        print(f"Translated: {translated!r}")

        # text to speech — both original and translated
        original_audio_b64 = make_tts(text, fix_lang(src_lang))
        audio_b64 = make_tts(translated, tgt_lang)

        return jsonify({
            'original_text': text,
            'translated_text': translated,
            'src_lang': src_lang,
            'tgt_lang': tgt_lang,
            'confidence': float(confidence),
            'original_audio_b64': original_audio_b64,
            'audio_b64': audio_b64
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
