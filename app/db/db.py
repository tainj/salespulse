import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base  # твои модели

# Указываем абсолютный путь к БД — внутри твоей домашней директории
DB_PATH = "/home/tainj/salespulse/db/store.db"

# Создаём папку db, если её нет
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Формируем URL с абсолютным путём
DATABASE_URL = f"sqlite:///{DB_PATH}"

logger = logging.getLogger(__name__)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    return SessionLocal()

def init_db():
    Base.metadata.create_all(engine)
    logger.info("✅ Таблицы созданы в базе данных.")