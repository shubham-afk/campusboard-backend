# schemas.py
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
