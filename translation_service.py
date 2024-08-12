from googletrans import Translator

class TranslationService:
    def __init__(self):
        self.translator = Translator()

    def translate_curriculum(self, content_dict, target_lang):
        translated_content = {}
        for key, value in content_dict.items():
            if isinstance(value, str):
                translated_content[key] = self.translator.translate(value, dest=target_lang).text
            elif isinstance(value, dict):
                translated_content[key] = {k: self.translator.translate(v, dest=target_lang).text for k, v in value.items()}
        return translated_content
