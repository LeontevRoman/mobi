from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base


class ImageUpload(Base):
    __tablename__ = "imageupload"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String)
    timestamp = Column(DateTime, unique=True, default=datetime.now())
    description = Column(String)
    comment = Column(String)
