import gettext
from fastapi import Request

LOCALES = ["en", "fr"]
DEFAULT_LANG = "en"
LOCALE_DIR = "i18n"

def detect_language(request: Request) -> str:
    accept_language = request.headers.get("accept-language", "")
    for lang in accept_language.split(","):
        code = lang.split(";")[0].strip()
        if code in LOCALES:
            return code
    return DEFAULT_LANG

def get_translator(lang: str):
    try:
        return gettext.translation("messages", localedir=LOCALE_DIR, languages=[lang])
    except FileNotFoundError:
        return gettext.NullTranslations()
