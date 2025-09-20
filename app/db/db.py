from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base  # импортируем модели
import logging

DATABASE_URL = "sqlite:///db/store.db"
logger = logging.getLogger(__name__)

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    return SessionLocal()

def init_db():
    Base.metadata.create_all(engine)
    logger.info("✅ Таблицы созданы в базе данных.")