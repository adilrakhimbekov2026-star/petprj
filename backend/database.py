from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Берем URL базы из переменных окружения (которые мы прописали в docker-compose)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/mydatabase")

# Engine — это "пульт управления" подключением
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal — это класс для создания сессий (одна сессия на один запрос)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

# Функция-зависимость для получения доступа к БД в эндпоинтах
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()