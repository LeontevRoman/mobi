from fastapi import APIRouter
from app.routes.image import image_check
from app.wsgi import app


app.include_router(image_check, prefix="/api/v1/mobi-test")
