# models.py
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

    # NEW fields for claim-review workflow
    # who requested the claim (stores username while pending)
    claim_requested_by = Column(String, nullable=True)
    # possible values: 'none' | 'pending' | 'approved' | 'rejected'
    claim_status = Column(String, nullable=False, default="none")

    # kept for backward compatibility: set when claim is approved
    claimed_by = Column(String, nullable=True)


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("username", name="uq_users_username"),)

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")  # "user" | "admin"
