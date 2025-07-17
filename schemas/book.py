from datetime import date
from pydantic import BaseModel

class BookCreate(BaseModel):
    name : str
    description : str
    author : str
    date_release : date
    is_available : bool
    id_lending : int

class BookOut(BaseModel):
    id : int
    name : str
    description : str
    author : str
    date_release : date
    is_available : bool
    id_lending : int

    class Config:
        orm_mode = True