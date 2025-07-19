from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.jwt import get_db
from models.book import Book
from models.lending import Lending
from schemas.lending import LendingCreate, LendingOut


router = APIRouter(prefix="/lending", tags=["lending"])

@router.post("/register", response_model = LendingCreate)
def register_lend(lend: LendingCreate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == lend.id_book).first()    
    if not book:
        raise HTTPException(status_code=404, detail="El libro no existe")

    if not book.is_available:
        raise HTTPException(status_code=400, detail="El libro no está disponible")

    new_lend = Lending(start_date=lend.start_date, end_date=lend.end_date, id_user=lend.id_user, id_book=lend.id_book) 
    db.add(new_lend) #lo agrego a la db tipo insert
    book.is_available = False
    db.commit() 
    db.refresh(new_lend)
    return new_lend 

@router.get("/list", response_model = List[LendingOut])
def list_lend(db: Session = Depends(get_db)):
    return db.query(Lending).all()