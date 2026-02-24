from googletrans import Translator

translator = Translator()

def translate(text, lang):
    if lang == "en":
        return text
    return translator.translate(text, dest=lang).text
