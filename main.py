from fastapi import FastAPI
from database import Base, engine
from routers import auth

#Para crear las tablas de la bd 
Base.metadata.create_all(bind=engine)

# Creamos la app
app = FastAPI()

#Incluimos los routers
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "La app funciona correctamente"}