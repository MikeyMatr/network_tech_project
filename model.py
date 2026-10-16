from typing import List, Optional

from fastapi import Form, HTTPException
from pydantic import BaseModel, ConfigDict, Field


class TodoItem(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    item: str = Field(..., min_length=1, description="Текст задачи")


class Todo(TodoItem):
    # Форма не передаёт ID: маршрутизатор назначает его перед сохранением.
    id: Optional[int] = Field(default=None, gt=0, description="Идентификатор задачи")

    @classmethod
    def as_form(cls, item: str = Form(..., min_length=1)):
        item = item.strip()
        if not item:
            raise HTTPException(status_code=422, detail="Текст задачи не должен быть пустым")
        return cls(item=item)


class TodoItems(BaseModel):
    developer: str = "MikeyKknv"
    todos: List[TodoItem]


class MessageResponse(BaseModel):
    status: str
    developer: str
    message: str
