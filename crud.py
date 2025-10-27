# # crud.py
# from sqlalchemy.orm import Session
# # from . import models, schemas
# import models
# import schemas


# def get_notices(db: Session):
#     return db.query(models.Notice).all()

# def get_notice(db: Session, notice_id: int):
#     return db.query(models.Notice).filter(models.Notice.id == notice_id).first()

# def create_notice(db: Session, notice: schemas.NoticeCreate):
#     db_notice = models.Notice(**notice.dict())
#     db.add(db_notice)
#     db.commit()
#     db.refresh(db_notice)
#     return db_notice

# def delete_notice(db: Session, notice_id: int):
#     notice = db.query(models.Notice).filter(models.Notice.id == notice_id).first()
#     if notice:
#         db.delete(notice)
#         db.commit()
#     return notice

# def claim_notice(db: Session, notice_id: int, username: str):
#     notice = db.query(models.Notice).filter(models.Notice.id == notice_id).first()
#     if not notice:
#         return None
#     if notice.claimed_by:  # already claimed
#         return False
#     notice.claimed_by = username
#     db.commit()
#     db.refresh(notice)
#     return notice

# def get_claimed_notices(db: Session):
#     return db.query(models.Notice).filter(models.Notice.claimed_by.isnot(None)).all()


# from sqlalchemy.orm import Session
# import models
# import schemas
# from passlib.context import CryptContext


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def hash_password(password: str) -> str:
#     return pwd_context.hash(password)


# def verify_password(plain: str, hashed: str) -> bool:
#     return pwd_context.verify(plain, hashed)


# # ----- Notices (existing) -----


# def get_notices(db: Session):
#     return db.query(models.Notice).all()


# def get_notice(db: Session, notice_id: int):
#     return db.query(models.Notice).filter(models.Notice.id == notice_id).first()


# def create_notice(db: Session, notice: schemas.NoticeCreate):
#     db_notice = models.Notice(**notice.dict())
#     db.add(db_notice)
#     db.commit()
#     db.refresh(db_notice)
#     return db_notice


# def delete_notice(db: Session, notice_id: int):
#     notice = db.query(models.Notice).filter(models.Notice.id == notice_id).first()
#     if notice:
#         db.delete(notice)
#         db.commit()
#     return notice


# def claim_notice(db: Session, notice_id: int, username: str):
#     notice = db.query(models.Notice).filter(models.Notice.id == notice_id).first()
#     if not notice:
#         return None
#     if notice.claimed_by:  # already claimed
#         return False
#     notice.claimed_by = username
#     db.commit()
#     db.refresh(notice)
#     return notice


# def get_claimed_notices(db: Session):
#     return db.query(models.Notice).filter(models.Notice.claimed_by.isnot(None)).all()


# # ----- Users -----


# def get_user_by_username(db: Session, username: str) -> models.User | None:
#     return db.query(models.User).filter(models.User.username == username).first()


# def create_user(db: Session, username: str, password: str, role: str = "user") -> models.User:
#     user = models.User(username=username, password_hash=hash_password(password), role=role)
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user



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

def claim_notice(db: Session, notice_id: int, username: str):
    notice = db.query(models.Notice).filter(models.Notice.id == notice_id).first()
    if not notice:
        return None
    if notice.claimed_by:
        return False
    notice.claimed_by = username
    db.commit()
    db.refresh(notice)
    return notice

def get_claimed_notices(db: Session):
    return db.query(models.Notice).filter(models.Notice.claimed_by.isnot(None)).all()

# --- Users CRUD ---
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, username: str, password: str, role: str = "user"):
    user = models.User(username=username, password_hash=hash_password(password), role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
