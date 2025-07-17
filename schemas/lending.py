from datetime import date
from pydantic import BaseModel

class LendingCreate(BaseModel):
    start_date : date
    end_date : date
    id_user : int

class LendingOut(BaseModel):
    id : int
    start_date : date
    end_date : date
    id_user : int

    class Config:
        orm_mode = True