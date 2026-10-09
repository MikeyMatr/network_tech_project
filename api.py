from fastapi import FastAPI
from todo import todo_router

app = FastAPI(
    title="Практическая работа: CRUD-приложение, модели ответов и обработка ошибок",
    description="Демонстрация работы с APIRouter, response_model, HTTPException и кастомными кодами статуса.",
    version="2.0.0"
)

@app.get("/", tags=["Главная"])
async def root():
    return {
        "project": "FastAPI CRUD Service",
        "developer": "Иванов Иван",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

# Подключение маршрутизатора
app.include_router(todo_router)