from model import get_model

# Initial prompts in each language's native script.
# This tells Whisper what script to output in, which fixes cases where
# it outputs Devanagari for Telugu/Tamil/etc speech.
SCRIPT_PROMPTS = {
    'te': 'ఈ వాక్యం తెలుగులో ఉంది.',
    'ta': 'இந்த வாக்கியம் தமிழில் உள்ளது.',
    'hi': 'यह वाक्य हिंदी में है।',
    'ar': 'هذه الجملة باللغة العربية.',
    'zh': '这句话是中文。',
    'ja': 'この文は日本語です。',
    'ko': '이 문장은 한국어입니다.',
    'ru': 'Это предложение на русском языке.',
    'de': 'Dieser Satz ist auf Deutsch.',
    'fr': 'Cette phrase est en français.',
    'es': 'Esta frase está en español.',
}

def get_text(audio, lang=None):
    model = get_model()
    options = {
        "task": "transcribe",
        "beam_size": 5,
        "fp16": False,
        "condition_on_previous_text": False,
        "no_speech_threshold": 0.4,
        "logprob_threshold": -1.0,
    }
    if lang:
        options["language"] = lang
        if lang in SCRIPT_PROMPTS:
            options["initial_prompt"] = SCRIPT_PROMPTS[lang]
    result = model.transcribe(audio, **options)
    return result["text"].strip()
