from gtts import gTTS
import os
import platform


def play(text, lang):
    """
    Generate TTS audio and play it locally.
    This is the standalone desktop version — the Flask app uses
    generate_tts() in app.py which returns base64 instead of playing.
    """
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save('out.mp3')

    system = platform.system()
    if system == 'Windows':
        os.system('start out.mp3')
    elif system == 'Darwin':
        os.system('afplay out.mp3')
    else:
        os.system('mpg123 out.mp3 2>/dev/null')
