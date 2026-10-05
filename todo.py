from fastapi import APIRouter, Path, HTTPException, status
from typing import List
from model import Todo, TodoItem

todo_router = APIRouter(tags=["Задачи (Todos)"])

todo_list: List[Todo] = []

AUTHOR_NAME = "Mike"


@todo_router.post("/todo", status_code=status.HTTP_201_CREATED)
async def add_todo(todo: Todo) -> dict:
    """Добавить"""
    for existing in todo_list:
        if existing.id == todo.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"[{AUTHOR_NAME}] Задача с ID {todo.id} уже существует!"
            )
    todo_list.append(todo)
    return {
        "status": "success",
        "author": AUTHOR_NAME,
        "message": f"Задача успешно добавлена пользователем {AUTHOR_NAME}.",
        "todo": todo
    }


@todo_router.get("/todo")
async def retrieve_todos() -> dict:
    """Получение полного списка задач"""
    return {
        "author": AUTHOR_NAME,
        "total": len(todo_list),
        "todos": todo_list
    }


@todo_router.get("/todo/{todo_id}")
async def get_single_todo(
    todo_id: int = Path(..., title="ID задачи", description="Идентификатор задачи для поиска", gt=0)
) -> dict:
    """Получение одной задачи по её ID"""
    for todo in todo_list:
        if todo.id == todo_id:
            return {
                "author": AUTHOR_NAME,
                "todo": todo
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"[{AUTHOR_NAME}] Задача с ID {todo_id} не найдена."
    )


@todo_router.put("/todo/{todo_id}")
async def update_todo(
    todo_data: TodoItem,
    todo_id: int = Path(..., title="ID задачи", gt=0)
) -> dict:
    """Обновление существующей задачи"""
    for todo in todo_list:
        if todo.id == todo_id:
            todo.item = todo_data.item
            return {
                "status": "success",
                "author": AUTHOR_NAME,
                "message": f"Задача {todo_id} успешно обновлена пользователем {AUTHOR_NAME}.",
                "todo": todo
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"[{AUTHOR_NAME}] Задача с ID {todo_id} для обновления не найдена."
    )


@todo_router.delete("/todo/{todo_id}")
async def delete_single_todo(
    todo_id: int = Path(..., title="ID задачи", gt=0)
) -> dict:
    """Удаление задачи по её ID"""
    for index, todo in enumerate(todo_list):
        if todo.id == todo_id:
            deleted_item = todo_list.pop(index)
            return {
                "status": "success",
                "author": AUTHOR_NAME,
                "message": f"Задача с ID {todo_id} успешно удалена.",
                "deleted": deleted_item
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"[{AUTHOR_NAME}] Задача с ID {todo_id} для удаления не найдена."
    )