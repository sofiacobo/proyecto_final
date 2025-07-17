from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.jwt import get_db
from models.book import Book
from models.lending import Lending
from schemas.book import BookCreate, BookOut


router = APIRouter(prefix="/books", tags=["books"])

@router.post("/register", response_model = BookOut)
def register_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = Book(name=book.name, description=book.description, author=book.author, date_release=book.date_release, is_available=book.is_available, id_lending=book.id_lending) 
    db.add(new_book) #lo agrego a la db tipo insert
    db.commit() 
    db.refresh(new_book)
    return new_book 

@router.get("/list", response_model = List[BookOut])
def list_books(db: Session = Depends(get_db)):
    return db.query(Book).all()
