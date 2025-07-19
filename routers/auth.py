from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth.hash import hash_password, verify_password
from auth.jwt import create_token, get_db
from models.user import User
from schemas.user import UserCreate, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first(): #valida si el mail ya existe
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    hashed = hash_password(user.password)
    nuevo = User(email=user.email, hashed_password=hashed) #creo un nuevo usuario con el mail y la pass hasheada
    db.add(nuevo) #lo agrego a la db tipo insert
    db.commit() 
    db.refresh(nuevo)
    return {"msg": "Usuario creado exitosamente"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales incorrectas",
        headers={"WWW-Authenticate": "Bearer"})
    user = db.query(User).filter(User.email == form_data.username).first() #traemos el usuario de la bd
    if not user or not verify_password(form_data.password, user.hashed_password): #si el user no existe o el pass no esta verificado
        raise credentials_exception
    # return {"msg": "Login correcto"}

    access_token = create_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/list", response_model = List[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()