from deep_translator import GoogleTranslator


def do_translate(text, from_lang, to_lang):
    """
    Translate text from from_lang to to_lang using Google Translator.
    Both codes should be ISO 639-1 (e.g. 'en', 'hi', 'fr').
    Returns translated string.
    """
    # deep_translator accepts 'auto' for source when unsure
    src = from_lang if from_lang else 'auto'
    translator = GoogleTranslator(source=src, target=to_lang)
    result = translator.translate(text)
    if not result:
        raise ValueError(f"Translation returned empty result ({from_lang} → {to_lang})")
    return result
