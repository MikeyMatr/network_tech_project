from fastapi import FastAPI
from todo import todo_router

app = FastAPI(
    title="Todo API — Практическое занятие №2",
    description="",
    version="alphabetamega"
)

# Корневой маршрут с персонализацией
@app.get("/", tags=["Главная"])
async def welcome() -> dict:
    return {
        "message": "Добро пожаловать в сервис управления задачами!",
        "author": "Студент",
        "docs_url": "/docs"
    }

app.include_router(todo_router)