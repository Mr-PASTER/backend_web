from fastapi import FastAPI

from app.db import init_db
from app.routers import levers, projects

app = FastAPI(
    title="Lever Control API",
    description="API для управления рычагами",
    version="1.0.0"
)

# Подключение роутеров
app.include_router(levers.router)
app.include_router(projects.router)


@app.on_event("startup")
async def on_startup():
    """Создание таблиц БД при запуске приложения."""
    init_db()


@app.get("/")
async def root():
    """Корневой endpoint"""
    return {
        "message": "Добро пожаловать в API управления рычагами",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Проверка здоровья API"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=4000,
        reload=True,
    )