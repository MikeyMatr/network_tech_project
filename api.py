from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from todo import todo_router

app = FastAPI(
    title="Практическая работа №5: шаблоны в FastAPI",
    description="Список задач с HTML-формой и наследованием шаблонов Jinja2.",
    version="3.0.0",
)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/todo", status_code=303)


app.include_router(todo_router)
