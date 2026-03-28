from deep_translator import GoogleTranslator

def do_translate(text, from_lang, to_lang):
    src = from_lang if from_lang else 'auto'
    result = GoogleTranslator(source=src, target=to_lang).translate(text)
    if not result:
        raise ValueError("Translation came back empty")
    return result
