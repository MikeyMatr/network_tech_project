from pydantic import BaseModel, Field
from typing import Optional


class TodoItem(BaseModel):
    """Модель отдельной задачи (для обновления или вложенности)"""
    item: str = Field(..., description="Текст задачи")

    class Config:
        schema_extra = {
            "example": {
                "item": "Завершить практическую работу №2"
            }
        }
        json_schema_extra = {
            "example": {
                "item": "Завершить практическую работу №2"
            }
        }


class Todo(BaseModel):
    """Основная модель задачи с идентификатором"""
    id: int = Field(..., description="Уникальный идентификатор задачи", gt=0)
    item: str = Field(..., description="Описание задачи")

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "item": "Изучать"
            }
        }
        json_schema_extra = {
            "example": {
                "id": 1,
                "item": "Изучать"
            }
        }