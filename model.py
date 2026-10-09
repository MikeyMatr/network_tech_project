from typing import List, Optional
from pydantic import BaseModel, Field



class TodoItem(BaseModel):
    item: str = Field(..., description="Текст задачи")

    class Config:
        schema_extra = {
            "example": {
                "item": "Изучить модели ответов и HTTPException в FastAPI"
            }
        }
        json_schema_extra = schema_extra

class Todo(BaseModel):
    id: int = Field(..., gt=0, description="Уникальный идентификатор задачи")
    item: str = Field(..., description="Текст задачи")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "item": "Сдать практическую работу по FastAPI"
            }
        }
        json_schema_extra = json_schema_extra


class TodoItems(BaseModel):
    developer: str = Field(default="Студент (Разработчик)", description="Имя разработчика")
    todos: List[TodoItem]

    class Config:
        schema_extra = {
            "example": {
                "developer": "Михаил",
                "todos": [
                    {"item": "Первая задача"},
                    {"item": "Вторая задача"}
                ]
            }
        }
        json_schema_extra = schema_extra


class MessageResponse(BaseModel):
    status: str
    developer: str
    message: str