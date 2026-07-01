from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import crud
from db.db import get_db
import schemas

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=List[schemas.Category])
def get_categories(db: Session = Depends(get_db)):
    """Список всех категорий"""
    return crud.get_categories(db)

@router.get("/{category_id}", response_model=schemas.Category)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Получить категорию по id"""
    category = crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/", response_model=schemas.Category, status_code=201)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """Создать категорию"""
    return crud.create_category(db, title=category.title)

@router.put("/{category_id}", response_model=schemas.Category)
def update_category(category_id: int, category: schemas.CategoryUpdate, db: Session = Depends(get_db)):
    """Обновить категорию"""
    updated = crud.update_category(db, category_id=category_id, title=category.title)
    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Удалить категорию"""
    if crud.delete_category(db, category_id):
        return {"message": "Category deleted successfully"}
    raise HTTPException(status_code=404, detail="Category not found")