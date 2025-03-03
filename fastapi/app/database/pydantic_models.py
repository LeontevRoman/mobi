from datetime import datetime
from pydantic import BaseModel, validator

""" Модели дял сериализации данных в ответах"""

class ImageUploadResponse(BaseModel):
    id: int
    file_name: str
    timestamp: str
    description: str
    status: str

    @validator('timestamp', pre=True)
    def format_timestamp(cls, value):
        if isinstance(value, datetime):
            return value.strftime("%d-%m-%Y %H:%M:%S")
        return value

    class Config:
        from_attributes = True  # Для совместимости с SQLAlchemy