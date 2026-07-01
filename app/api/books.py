from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import crud
from db.db import get_db
import schemas

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=List[schemas.Book])
def get_books(
    category_id: Optional[int] = Query(None, description="Filter by category_id"),
    db: Session = Depends(get_db)
):
    """Список всех книг (можно фильтровать по category_id)"""
    if category_id:
        if not crud.get_category(db, category_id):
            raise HTTPException(status_code=404, detail="Category not found")
        return crud.get_books_by_category(db, category_id)
    return crud.get_books(db)

@router.get("/{book_id}", response_model=schemas.BookWithCategory)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Получить книгу по id с информацией о категории"""
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=schemas.Book, status_code=201)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """Создать книгу (проверяем существование категории)"""
    if not crud.get_category(db, book.category_id):
        raise HTTPException(status_code=404, detail="Category not found")
    
    return crud.create_book(
        db=db,
        title=book.title,
        description=book.description,
        price=book.price,
        category_id=book.category_id,
        url=book.url
    )

@router.put("/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    """Обновить книгу (проверяем существование категории)"""
    existing_book = crud.get_book(db, book_id)
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if book.category_id and not crud.get_category(db, book.category_id):
        raise HTTPException(status_code=404, detail="Category not found")
    
    updated = crud.update_book(
        db=db,
        book_id=book_id,
        title=book.title,
        description=book.description,
        price=book.price,
        url=book.url
    )
    return updated

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Удалить книгу"""
    if crud.delete_book(db, book_id):
        return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")