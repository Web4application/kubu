from fastapi import FastAPI, Request
from fastapi.routing import APIRouter
from utils.i18n import get_locale, get_translator

app = FastAPI()

def localized_router(lang: str):
    router = APIRouter()

    @router.get("/advanced")
    def advanced_page(request: Request):
        translator = get_translator(lang)
        _ = translator.gettext
        return {"message": _(f"Welcome to the advanced Kubuverse page in {lang}")}

    return router

# Mount localized routes
for lang in ["en", "fr"]:
    app.include_router(localized_router(lang), prefix=f"/{lang}")
