import gettext
from pathlib import Path
from fastapi import Request

LOCALE_PATH = Path("i18n")

def get_locale(request: Request) -> str:
    return request.path_params.get("lang", "en")

def get_translator(lang: str):
    locale_dir = str(LOCALE_PATH.resolve())
    try:
        return gettext.translation("messages", localedir=locale_dir, languages=[lang])
    except FileNotFoundError:
        return gettext.NullTranslations()
