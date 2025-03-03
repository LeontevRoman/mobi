import logging
from logging.handlers import RotatingFileHandler
import os

# Создаем директорию для логов, если она не существует
log_dir = os.path.join("app", "logs")
os.makedirs(log_dir, exist_ok=True)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    handlers=[
        RotatingFileHandler(
            os.path.join(log_dir, "app.log"), 
            encoding='utf-8', 
            maxBytes=10 * 1024 * 1024, 
            backupCount=5  
        ),
        logging.StreamHandler() 
    ]
)

logger = logging.getLogger(__name__)
