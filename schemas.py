# # schemas.py
# from pydantic import BaseModel

# class NoticeBase(BaseModel):
#     title: str
#     author: str
#     department: str
#     category: str
#     date: str
#     time: str
#     claimed_by: str | None = None

# class NoticeCreate(NoticeBase):
#     pass

# class Notice(NoticeBase):
#     id: int

#     class Config:
#         orm_mode = True

from pydantic import BaseModel


class NoticeBase(BaseModel):
    title: str
    author: str
    department: str
    category: str
    date: str
    time: str
    claimed_by: str | None = None


class NoticeCreate(NoticeBase):
    pass


class Notice(NoticeBase):
    id: int
    class Config:
        orm_mode = True


# --- Auth/User ---
class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    username: str
    role: str


class LoginRequest(BaseModel):
    username: str
    password: str