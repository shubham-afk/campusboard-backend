# crud.py
from sqlalchemy.orm import Session
import models
import schemas
from passlib.context import CryptContext

# Use PBKDF2-SHA256 to avoid bcrypt's 72-byte limit
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# --- Notices CRUD ---
def get_notices(db: Session):
    return db.query(models.Notice).all()


def get_notice(db: Session, notice_id: int):
    return db.query(models.Notice).filter(models.Notice.id == notice_id).first()


def create_notice(db: Session, notice: schemas.NoticeCreate):
    db_notice = models.Notice(**notice.dict())
    db.add(db_notice)
    db.commit()
    db.refresh(db_notice)
    return db_notice


def delete_notice(db: Session, notice_id: int):
    notice = db.query(models.Notice).filter(models.Notice.id == notice_id).first()
    if notice:
        db.delete(notice)
        db.commit()
    return notice


# Request a claim (user requests -> sets claim_requested_by + claim_status='pending')
def request_claim(db: Session, notice_id: int, username: str):
    notice = db.query(models.Notice).filter(models.Notice.id == notice_id).first()
    if not notice:
        return None
    # if already approved (claimed) -> cannot request
    if notice.claim_status == "approved" or notice.claimed_by:
        return False
    # if there's already a pending request -> conflict
    if notice.claim_status == "pending":
        return "conflict"
    notice.claim_requested_by = username
    notice.claim_status = "pending"
    db.commit()
    db.refresh(notice)
    return notice


# Admin: list pending claims
def get_pending_claims(db: Session):
    return db.query(models.Notice).filter(models.Notice.claim_status == "pending").all()


# Admin: approve claim -> set claimed_by, claim_status='approved', clear claim_requested_by
def approve_claim(db: Session, notice_id: int):
    notice = db.query(models.Notice).filter(models.Notice.id == notice_id).first()
    if not notice:
        return None
    if notice.claim_status != "pending" or not notice.claim_requested_by:
        return False
    notice.claimed_by = notice.claim_requested_by
    notice.claim_status = "approved"
    notice.claim_requested_by = None
    db.commit()
    db.refresh(notice)
    return notice


# Admin: reject claim -> set claim_status='rejected', clear claim_requested_by
def reject_claim(db: Session, notice_id: int):
    notice = db.query(models.Notice).filter(models.Notice.id == notice_id).first()
    if not notice:
        return None
    if notice.claim_status != "pending":
        return False
    notice.claim_status = "rejected"
    notice.claim_requested_by = None
    db.commit()
    db.refresh(notice)
    return notice


# Existing: get approved / claimed items (used by ClaimedItems page)
def get_claimed_notices(db: Session):
    return db.query(models.Notice).filter(models.Notice.claim_status == "approved").all()


# --- Users CRUD ---
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, username: str, password: str, role: str = "user"):
    user = models.User(username=username, password_hash=hash_password(password), role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
