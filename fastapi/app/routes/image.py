from datetime import datetime
import io
import traceback
from typing import List

from fastapi import APIRouter, HTTPException, UploadFile
from PIL import Image
from pydantic import BaseModel
from sqlalchemy import desc
from transformers import BlipProcessor, BlipForConditionalGeneration, MarianMTModel, MarianTokenizer

from app.database import SessionLocal
from app.database.models import ImageUpload
from app.database.pydantic_models import ImageUploadResponse

image_check = APIRouter(prefix="/image")

@image_check.post("/create-description")
async def image_create_description(file: UploadFile):
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
        
        # Загрузка модели и процессора
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        
        # Генерация описания
        inputs = processor(image_content, return_tensors="pt")
        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)

        # А если по-русски
        model_name = "Helsinki-NLP/opus-mt-en-ru"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        inputs = tokenizer(caption, return_tensors="pt", max_length=512, truncation=True)
        translated = model.generate(**inputs)
        russian_text = tokenizer.decode(translated[0], skip_special_tokens=True)

        # Создание записи в базе данных
        db_image = ImageUpload(
            file_name=file.filename,
            description=russian_text,
            timestamp=datetime.now(),
            comment='Обработано успешно'
        )
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        
        return {"description": russian_text}
    except Exception as exc:
        db_image = ImageUpload(
            file_name=file.filename,
            description='Не удалось обработать изображение',
            timestamp=datetime.now(),
            comment=str(exc)
        )
        db.add(db_image)
        db.commit()
        db.refresh(db_image)

        print(traceback.print_exc())
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
        print(traceback.print_exc())
        raise HTTPException(status_code=400, detail=str(exc))
    finally:
        db.close()  