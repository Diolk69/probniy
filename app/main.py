from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

from db.db import engine
from db import models
from db import crud

load_dotenv()

def print_data():
    """Выводим все данные из базы"""
    
    print("=" * 60)
    print("БАЗА ДАННЫХ КНИГ")
    print("=" * 60)
    
    db = Session(bind=engine)
    
    try:
        print("\nКАТЕГОРИИ:")
        print("-" * 60)
        categories = crud.get_categories(db)
        
        for cat in categories:
            print(f"ID: {cat.id} | Название: {cat.title}")
        
        print("\nКНИГИ:")
        print("-" * 60)
        books = crud.get_books(db)
        
        for book in books:
            category = crud.get_category(db, book.category_id)
            print(f"\nID: {book.id}")
            print(f"Название: {book.title}")
            print(f"Описание: {book.description}")
            print(f"Цена: {book.price} руб.")
            print(f"Категория: {category.title if category else 'N/A'}")
            print(f"URL: {book.url if book.url else 'не указан'}")
        
        print("\n" + "=" * 60)
        print(f"Всего категорий: {len(categories)}")
        print(f"Всего книг: {len(books)}")
        print("=" * 60)
        
    finally:
        db.close()

if __name__ == "__main__":
    print_data()