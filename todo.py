from fastapi import APIRouter, Path, HTTPException, status
from typing import List
from model import Todo, TodoItem, TodoItems, MessageResponse

todo_router = APIRouter(prefix="/todo", tags=["Управление задачами (Todo CRUD)"])

todo_list: List[Todo] = []

DEVELOPER_NAME = "MikeyKknv"


@todo_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=MessageResponse,
    summary="Добавить новую задачу"
)
async def add_todo(todo: Todo):

    for existing_todo in todo_list:
        if existing_todo.id == todo.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"[{DEVELOPER_NAME}] Ошибка: задача с ID {todo.id} уже зарегистрирована в системе."
            )
    todo_list.append(todo)
    return MessageResponse(
        status="success",
        developer=DEVELOPER_NAME,
        message=f"Задача #{todo.id} успешно добавлена разработчиком {DEVELOPER_NAME}."
    )


@todo_router.get(
    "",
    response_model=TodoItems,
    status_code=status.HTTP_200_OK,
    summary="Получить список задач (только текст без ID)"
)
async def retrieve_todos():
    return TodoItems(
        developer=DEVELOPER_NAME,
        todos=[TodoItem(item=t.item) for t in todo_list]
    )


@todo_router.get(
    "/{todo_id}",
    status_code=status.HTTP_200_OK,
    summary="Получить задачу по ID"
)
async def get_single_todo(
    todo_id: int = Path(..., title="ID задачи", description="Идентификатор задачи", gt=0)
) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            return {
                "developer": DEVELOPER_NAME,
                "todo": todo
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"[{DEVELOPER_NAME}] Задача с идентификатором {todo_id} не найдена."
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