from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.jwt import get_db
from models.book import Book
from schemas.book import BookCreate, BookOut, BookUpdate


router = APIRouter(prefix="/books", tags=["books"])

@router.post("/register", response_model = BookOut)
def register_book(book: BookCreate, db: Session = Depends(get_db)):
    try:
        new_book = Book(name=book.name, description=book.description, author=book.author, date_release=book.date_release, is_available=book.is_available) 
        db.add(new_book) #lo agrego a la db tipo insert
        db.commit() 
        db.refresh(new_book)
        return new_book 
    except Exception as e:
        print("Error en la conexión", e)

@router.get("/list", response_model = List[BookOut])
def list_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@router.delete("/delete/{id}")
def delete_book(id:int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == id).first() #trae una instancia de Book con el id especificado en la ruta

    if not book:
        raise HTTPException(status_code=404, detail="El libro no existe")
    db.delete(book) #eliminamos el libro de la tabla de la bd
    db.commit()
    return {"mensaje": "Libro eliminado con éxito"}

@router.put("/update/{id}")
def update_book(id:int, book_update:BookUpdate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == id).first()

    if not book:
        raise HTTPException(status_code=404, detail="El libro no existe")
    
    if book_update.is_available is not None:
        book.is_available = book_update.is_available

    db.commit()
    db.refresh(book)
    return {"mensaje": "El libro se actualizó correctamente"}

