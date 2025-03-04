
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from transformers import BlipProcessor, BlipForConditionalGeneration, MarianMTModel, MarianTokenizer


from app.database import Base, engine
# from app.routers import tags_metadata, mobi_test
from app.logging import logger


# Функция для управления жизненным циклом приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Загружаем модели при старте приложения
    app.state.blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    app.state.blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    app.state.marian_tokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-ru")
    app.state.marian_model = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-en-ru")
    print("Модели загружены!")
    yield  # Приложение запущено и готово к работе
    print("Приложение завершает работу...")

tags_metadata = [
    {
        "name": "Image",
        "description": "Создание текствого описания изображения",
    },
]

app = FastAPI(description=f"Mobi Test API", 
              title="Mobi Test API", 
              version="1.0.0", 
              openapi_tags=tags_metadata,
              lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"]
)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Входящий запрос: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"Ответ: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Ошибка при обработке запроса: {e}", exc_info=True)
        raise


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')

from . import routers
from . import database
