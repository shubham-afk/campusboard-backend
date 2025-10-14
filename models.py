# models.py
from sqlalchemy import Column, Integer, String
# from .database import Base
from database import Base 

class Notice(Base):
    __tablename__ = "notices"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    department = Column(String)
    category = Column(String)
    date = Column(String)
    time = Column(String)
    claimed_by = Column(String, nullable=True) 
