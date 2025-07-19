from fastapi import FastAPI
from database import Base, engine
from routers import auth, books, lending

# #Para borrar las tablas de la bd en caso de error en el modelo de datos
Base.metadata.drop_all(bind=engine)
#Para crear las tablas de la bd 
Base.metadata.create_all(bind=engine)

# Creamos la app
app = FastAPI()

#Incluimos los routers
app.include_router(auth.router)
app.include_router(books.router)
app.include_router(lending.router)

@app.get("/")
def read_root():
    return {"message": "La app funciona correctamente"}