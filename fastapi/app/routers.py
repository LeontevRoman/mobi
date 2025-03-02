from fastapi import APIRouter
from app.routes.image import image_check

mobi_test = APIRouter(prefix="/api/v1/mobi-test")

tags_metadata = [
    {
        "name": "Image",
        "description": "Создание текствого описания изображения",
    },
]

mobi_test.include_router(image_check, tags=["Image"])