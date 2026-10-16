from pathlib import Path as FilePath
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from model import MessageResponse, Todo, TodoItem


todo_router = APIRouter(prefix="/todo", tags=["Управление задачами"])
todo_list: List[Todo] = []
DEVELOPER_NAME = "MikeyKknv"

# Абсолютный путь позволяет находить шаблоны независимо от рабочей папки.
templates = Jinja2Templates(directory=str(FilePath(__file__).resolve().parent / "templates"))


@todo_router.post("", response_class=HTMLResponse, summary="Добавить задачу из формы")
async def add_todo(request: Request, todo: Todo = Depends(Todo.as_form)):
    todo.id = max((task.id for task in todo_list), default=0) + 1
    todo_list.append(todo)
    # После отправки формы открываем GET: обновление страницы не повторит POST.
    return RedirectResponse(url=request.url_for("retrieve_todos"), status_code=303)


@todo_router.get("", response_class=HTMLResponse, summary="Показать список задач")
async def retrieve_todos(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="todo.html",
        context={"todos": todo_list, "developer": DEVELOPER_NAME},
    )


@todo_router.get("/{todo_id}", response_class=HTMLResponse, summary="Показать задачу")
async def get_single_todo(request: Request, todo_id: int = Path(..., gt=0)):
    for todo in todo_list:
        if todo.id == todo_id:
            return templates.TemplateResponse(
                request=request,
                name="todo.html",
                context={"todo": todo, "developer": DEVELOPER_NAME},
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"[{DEVELOPER_NAME}] Задача с идентификатором {todo_id} не найдена.",
    )


@todo_router.put(
    "/{todo_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновить текст задачи"
)
async def update_todo(
    todo_data: TodoItem,
    todo_id: int = Path(..., title="ID задачи", gt=0)
):
    for todo in todo_list:
        if todo.id == todo_id:
            todo.item = todo_data.item
            return MessageResponse(
                status="success",
                developer=DEVELOPER_NAME,
                message=f"Задача #{todo_id} успешно обновлена разработчиком {DEVELOPER_NAME}."
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"[{DEVELOPER_NAME}] Невозможно обновить: задача с ID {todo_id} отсутствует."
    )


@todo_router.delete(
    "/{todo_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Удалить задачу по ID"
)
async def delete_single_todo(
    todo_id: int = Path(..., title="ID задачи", gt=0)
):
    for index, todo in enumerate(todo_list):
        if todo.id == todo_id:
            todo_list.pop(index)
            return MessageResponse(
                status="success",
                developer=DEVELOPER_NAME,
                message=f"Задача #{todo_id} успешно удалена разработчиком {DEVELOPER_NAME}."
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"[{DEVELOPER_NAME}] Невозможно удалить: задача с ID {todo_id} не существует."
    )


@todo_router.delete(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Очистить все задачи"
)
async def delete_all_todos():
    todo_list.clear()
    return MessageResponse(
        status="success",
        developer=DEVELOPER_NAME,
        message=f"Все задачи были очищены разработчиком {DEVELOPER_NAME}."
    )