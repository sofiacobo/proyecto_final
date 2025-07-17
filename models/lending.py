from sqlalchemy import Column, Date, ForeignKey, Integer
from database import Base

class Lending(Base):
    __tablename__ = "lending"
    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date)
    end_date = Column(Date)
    id_user = Column(Integer, ForeignKey("user.id"))
    