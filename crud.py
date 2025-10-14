# crud.py
from sqlalchemy.orm import Session
# from . import models, schemas
import models
import schemas


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
    if notice.claimed_by:  # already claimed
        return False
    notice.claimed_by = username
    db.commit()
    db.refresh(notice)
    return notice

def get_claimed_notices(db: Session):
    return db.query(models.Notice).filter(models.Notice.claimed_by.isnot(None)).all()

