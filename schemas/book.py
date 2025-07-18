from datetime import date
from pydantic import BaseModel

class BookCreate(BaseModel):
    name : str
    description : str
    author : str
    date_release : date
    is_available : bool

class BookOut(BaseModel):
    id : int
    name : str
    description : str
    author : str
    date_release : date
    is_available : bool

    class Config:
        from_attributes = True