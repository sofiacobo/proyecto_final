from datetime import UTC, datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from database import SessionLocal
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from models.user import User

SECRET_KEY = "3TkpHoef4X-uNndG0L_E2h-aW7jczPBiapEWfSnk9-g" #en el env, en cmd se ejecuta python -c "import secrets; print(secrets.token_urlsafe(32))"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 30 #minutos de expiracion del token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_token(data: dict): 
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=30) 
    to_encode.update({"exp": expire}) #al diccionario se le agrega el tiempo de expiracion, es decir los 30 min
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_db(): #crea la conexion
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException( 
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido",
        headers={"WWW-Authenticate": "Bearer"})

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) #decodifica el token con la secret key y el tipo de algoritmo
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first() 
    if user is None:
        raise credentials_exception 
    return user