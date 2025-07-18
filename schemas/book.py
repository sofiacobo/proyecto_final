from datetime import date
from typing import Optional
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

class BookUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    date_release: Optional[date] = None
    is_available: Optional[bool] = None

    class Config:
        from_attributes = True