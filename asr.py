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
    'pt': 'Esta frase está em português.',
    'it': 'Questa frase è in italiano.',
    'nl': 'Deze zin is in het Nederlands.',
    'pl': 'To zdanie jest po polsku.',
    'tr': 'Bu cümle Türkçedir.',
    'uk': 'Це речення українською мовою.',
    'id': 'Kalimat ini dalam bahasa Indonesia.',
    'vi': 'Câu này bằng tiếng Việt.',
    'th': 'ประโยคนี้เป็นภาษาไทย',
}

def get_text(audio, lang=None):
    model = get_model()
    options = {
        "task": "transcribe",
        "beam_size": 5,
        "fp16": False,
        "condition_on_previous_text": False,
        # Use temperature fallback: start with greedy, increase if needed
        "temperature": (0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
        # Looser thresholds — let Whisper return output even with lower confidence
        "no_speech_threshold": 0.6,
        "logprob_threshold": -2.0,
        "compression_ratio_threshold": 2.4,
    }
    if lang:
        options["language"] = lang
        if lang in SCRIPT_PROMPTS:
            options["initial_prompt"] = SCRIPT_PROMPTS[lang]
    result = model.transcribe(audio, **options)
    return result["text"].strip()
