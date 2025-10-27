# # models.py
# from sqlalchemy import Column, Integer, String
# # from .database import Base
# from database import Base 

# class Notice(Base):
#     __tablename__ = "notices"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String)
#     author = Column(String)
#     department = Column(String)
#     category = Column(String)
#     date = Column(String)
#     time = Column(String)
#     claimed_by = Column(String, nullable=True) 


from sqlalchemy import Column, Integer, String, UniqueConstraint
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


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("username", name="uq_users_username"),)

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user") # "user" | "admin"