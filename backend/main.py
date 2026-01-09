from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# 1. Настройка базы данных (Подключаемся к контейнеру 'db')
DATABASE_URL = "postgresql://user:password@db:5432/mydatabase"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Модель таблицы в БД (Как это хранится в Postgres)
class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)

# Создаем таблицы при запуске
Base.metadata.create_all(bind=engine)

# 3. Схема валидации (Что мы ждем от фронтенда)
class MessageCreate(BaseModel):
    content: str

# 4. Инициализация FastAPI
app = FastAPI()

# Настройка CORS (чтобы фронтенд мог достучаться)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ЭНДПОИНТЫ (Ручки) ---

# Сохранение текста
@app.post("/add")
def create_message(msg: MessageCreate, db: Session = Depends(get_db)):
    new_msg = Message(content=msg.content)
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    return {"status": "ok", "id": new_msg.id}

# Получение всех текстов
@app.get("/list")
def get_messages(db: Session = Depends(get_db)):
    messages = db.query(Message).all()
    return messages