import os

_translator = None


def get_translator():
    global _translator
    if _translator is None:
        try:
            from deep_translator import GoogleTranslator
            _translator = GoogleTranslator(source="en", target="vi")
        except Exception as e:
            print(f"  Warning: Cannot init translator: {e}")
            _translator = False
    return _translator if _translator is not False else None


def translate_text(text, src="en", dest="vi"):
    if not text or len(text.strip()) < 3:
        return text
    if os.environ.get("TRANSLATION_ENABLED", "1") != "1":
        return text
    translator = get_translator()
    if translator is None:
        return text
    try:
        result = translator.translate(text[:5000])
        if result:
            return result
        return text
    except Exception:
        return text
