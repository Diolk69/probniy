from sqlalchemy.orm import Session
from . import models

def get_categories(db: Session):
    """Получить все категории"""
    return db.query(models.Category).all()

def get_category(db: Session, category_id: int):
    """Получить категорию по ID"""
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def create_category(db: Session, title: str):
    """Создать категорию"""
    category = models.Category(title=title)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def update_category(db: Session, category_id: int, title: str):
    """Обновить категорию"""
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category:
        category.title = title
        db.commit()
        db.refresh(category)
    return category

def delete_category(db: Session, category_id: int):
    """Удалить категорию"""
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category:
        db.delete(category)
        db.commit()
        return True
    return False

def get_books(db: Session):
    """Получить все книги"""
    return db.query(models.Book).all()

def get_book(db: Session, book_id: int):
    """Получить книгу по ID"""
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books_by_category(db: Session, category_id: int):
    """Получить все книги категории"""
    return db.query(models.Book).filter(models.Book.category_id == category_id).all()

def create_book(db: Session, title: str, description: str, price: float, 
                category_id: int, url: str = ""):
    """Создать книгу"""
    book = models.Book(
        title=title,
        description=description,
        price=price,
        url=url,
        category_id=category_id
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def update_book(db: Session, book_id: int, title: str = None, 
                description: str = None, price: float = None, url: str = None):
    """Обновить книгу"""
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book:
        if title:
            book.title = title
        if description:
            book.description = description
        if price:
            book.price = price
        if url is not None:
            book.url = url
        db.commit()
        db.refresh(book)
    return book

def delete_book(db: Session, book_id: int):
    """Удалить книгу"""
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book:
        db.delete(book)
        db.commit()
        return True
    return False