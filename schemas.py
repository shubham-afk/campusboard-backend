# schemas.py
from pydantic import BaseModel


class NoticeBase(BaseModel):
    title: str
    author: str
    department: str
    category: str
    date: str
    time: str
    claim_requested_by: str | None = None
    claim_status: str = "none"
    claimed_by: str | None = None


class NoticeCreate(NoticeBase):
    # frontend still sends the same fields as before (backend manages claim fields)
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
