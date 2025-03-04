from datetime import datetime
import io
import traceback
from typing import List

from fastapi import APIRouter, Form, HTTPException, UploadFile
from PIL import Image
from sqlalchemy import desc


from app.database import SessionLocal
from app.database.models import ImageUpload
from app.database.pydantic_models import ImageUploadResponse
from app.logging import logger
from app.wsgi import app

image_check = APIRouter(prefix="/image", tags=["Image"])

@image_check.post("/create-description")
async def image_create_description(file: UploadFile, lang: str = Form(...)):
    """     
    **/api/v1/mobi-test/image/create-description** \n
    Создать описание изображения \n
    **:return:** json
    """
    db = SessionLocal()
    try:
         # Проверка типа изображения
        if not file.content_type.startswith("image/"):
            raise Exception("Неверный тип изображения")
        
        contents = await file.read()
        
        # Преобразование содержимого в объект изображения
        image_stream = io.BytesIO(contents)
        image_content = Image.open(image_stream).convert("RGB")
        
        # Генерация описания
        inputs = app.state.blip_processor(image_content, return_tensors="pt")
        out = app.state.blip_model.generate(**inputs)
        caption = app.state.blip_processor.decode(out[0], skip_special_tokens=True)

        # А если по-русски
        if lang.lower() == "true":
            model_name = "Helsinki-NLP/opus-mt-en-ru"
            tokenizer = app.state.marian_tokenizer.from_pretrained(model_name)
            model = app.state.marian_model.from_pretrained(model_name)
            inputs = tokenizer(caption, return_tensors="pt", max_length=512, truncation=True)
            translated = model.generate(**inputs)
            caption = tokenizer.decode(translated[0], skip_special_tokens=True)

        # Создание записи в базе данных
        db_image = ImageUpload(
            file_name=file.filename,
            description=caption,
            timestamp=datetime.now(),
            status='Обработано успешно'
        )
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        
        return {"description": caption}
    except Exception as exc:
        db_image = ImageUpload(
            file_name=file.filename,
            description='Не удалось обработать изображение',
            timestamp=datetime.now(),
            status=str(exc)
        )
        db.add(db_image)
        db.commit()
        db.refresh(db_image)

        logger.error(f"Ошибка при обработке запроса: {str(exc)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(exc))
    finally:
        await file.close()
        db.close()


@image_check.get("/all", response_model=List[ImageUploadResponse])
async def get_all():
    """     
    **/api/v1/mobi-test/image/all** \n
    Получить все загруженные изображения \n
    **:return:** Список объектов ImageUpload
    """ 
    db = SessionLocal()
    try:
        image_uploads = db.query(ImageUpload).order_by(desc(ImageUpload.timestamp)).all()
        return image_uploads
    except Exception as exc:
        logger.error(f"Ошибка при обработке запроса: {str(exc)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(exc))
    finally:
        db.close()  