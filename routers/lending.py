from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.jwt import get_current_user, get_db
from models.book import Book
from models.lending import Lending
from models.user import User
from schemas.lending import LendingCreate, LendingOut


router = APIRouter(prefix="/lending", tags=["lending"])

@router.post("/register", response_model = LendingCreate)
def register_lend(lend: LendingCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    book = db.query(Book).filter(Book.id == lend.id_book).first()   
    if not book:
        raise HTTPException(status_code=404, detail="El libro no existe")

    if not book.is_available:
        raise HTTPException(status_code=400, detail="El libro no está disponible")

    new_lend = Lending(start_date=lend.start_date, end_date=lend.end_date, id_user=user.id, id_book=lend.id_book) 
    db.add(new_lend) #lo agrego a la db tipo insert
    book.is_available = False
    db.commit() 
    db.refresh(new_lend)
    return new_lend 

@router.get("/list", response_model = List[LendingOut])
def list_lend(db: Session = Depends(get_db)):
    return db.query(Lending).all()

@router.post("/return/{id}")
def return_lend(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    lending = db.query(Lending).filter(Lending.id == id).first() #busca el préstamo por id

    if not lending:
        raise HTTPException(status_code=404, detail="El préstamo no existe")

    if lending.id_user != user.id:
        raise HTTPException(status_code=403, detail="El préstamo que intentas devolver no te pertenece") #Verifica que el préstamo pertenece al usuario autenticado

    book = db.query(Book).filter(Book.id == lending.id_book).first() #busco el libro asociado al préstamo
    
    book.is_available = True #devuelvo el libro marcandolo como disponible
    db.commit()
    return {"mensaje": "Libro devuelto con éxito"}