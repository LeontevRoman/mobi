import os

from sqlalchemy import create_engine
from app.database.models import Base
from sqlalchemy.orm import sessionmaker

from app.settings import Config

host = os.environ.get('DB_HOST', 'localhost')
port = os.environ.get('DB_PORT', '5433')

# URL подключения к PostgreSQL
DATABASE_URL = f"postgresql://{Config.DB_USER}:{Config.DB_PASSWORD}@{host}:{port}/{Config.DB_NAME}"

# Создание движка SQLAlchemy
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

# Создание сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
