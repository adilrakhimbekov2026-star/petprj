from pydantic import BaseModel

# То, что мы получаем от фронтенда (только текст)
class MessageCreate(BaseModel):
    content: str

# То, что мы возвращаем фронтенду (текст + ID из базы)
class MessageResponse(BaseModel):
    id: int
    content: str

    # Это важно! Говорит Pydantic работать с объектами SQLAlchemy (не только со словарями)
    class Config:
        from_attributes = True