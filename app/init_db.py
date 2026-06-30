from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

from db.db import engine, Base
from db import models
from db import crud

load_dotenv()

def init_database():
    """Создаем таблицы и наполняем данными"""
    
    Base.metadata.create_all(bind=engine)
    print("Таблицы созданы!")
    
    db = Session(bind=engine)
    
    try:
        category1 = crud.create_category(db, title="Фантастика")
        category2 = crud.create_category(db, title="Программирование")
        
        print(f"Создана категория: {category1.title}")
        print(f"Создана категория: {category2.title}")
        
        crud.create_book(
            db=db,
            title="Дюна",
            description="Эпическая научная фантастика о пустынной планете Арракис",
            price=599.99,
            category_id=category1.id,
            url=""
        )
        
        crud.create_book(
            db=db,
            title="Основание",
            description="Классика научной фантастики Айзека Азимова",
            price=450.00,
            category_id=category1.id,
            url=""
        )
        
        crud.create_book(
            db=db,
            title="Марсианин",
            description="История выживания астронавта на Марсе",
            price=520.50,
            category_id=category1.id,
            url=""
        )
        
        print("Добавлены 3 книги в категорию 'Фантастика'")
        
        crud.create_book(
            db=db,
            title="Изучаем Python",
            description="Полное руководство для начинающих",
            price=890.00,
            category_id=category2.id,
            url=""
        )
        
        crud.create_book(
            db=db,
            title="Алгоритмы",
            description="Построение и анализ алгоритмов",
            price=1200.00,
            category_id=category2.id,
            url=""
        )
        
        crud.create_book(
            db=db,
            title="Чистый код",
            description="Создание, анализ и рефакторинг кода",
            price=950.00,
            category_id=category2.id,
            url=""
        )
        
        print("Добавлены 3 книги в категорию 'Программирование'")
        
        print("\nБаза данных успешно заполнена!")
        
    finally:
        db.close()

if __name__ == "__main__":
    init_database()