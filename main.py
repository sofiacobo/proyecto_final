from fastapi import FastAPI
from database import Base, engine

#Para crear las tablas de la bd 
Base.metadata.create_all(bind=engine)

# Creamos la app
app = FastAPI()