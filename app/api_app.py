from fastapi import FastAPI
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api import books, categories
from db.db import engine, get_db
from db import models

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        db = next(get_db())
        db.execute("SELECT 1")
        print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")
    yield
    print("Shutting down...")

app = FastAPI(
    title="Book Store API",
    description="API для управления книгами и категориями",
    version="1.0",
    lifespan=lifespan
)

app.include_router(categories.router)
app.include_router(books.router)

@app.get("/")
def root():
    """Главная страница"""
    return {
        "message": "Book API is running!",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health():
    """Проверка здоровья сервиса"""
    return {
        "status": "ok",
        "service": "Book API",
        "database": "connected"
    }