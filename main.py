# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi import Header

# from . import models, schemas, crud
import models
import schemas
import crud
from database import SessionLocal, engine

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow frontend (React) to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "CampusBoard API running 🚀"}


@app.get("/notices", response_model=list[schemas.Notice])
def read_notices(db: Session = Depends(get_db)):
    return crud.get_notices(db)


@app.post("/notices", response_model=schemas.Notice)
def create_notice(notice: schemas.NoticeCreate, db: Session = Depends(get_db)):
    return crud.create_notice(db, notice)


@app.delete("/notices/{notice_id}")
def delete_notice(notice_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_notice(db, notice_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Notice not found")
    return {"message": "Deleted successfully"}

# Define a login request schema
class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(request: LoginRequest):
    """
    Simple hardcoded login:
    - admin/admin123 => admin role
    - anything else  => user role
    """
    if request.username == "admin" and request.password == "admin123":
        return {"username": "admin", "role": "admin"}
    elif request.username and request.password:
        # treat all other users as normal users
        return {"username": request.username, "role": "user"}
    else:
        raise HTTPException(status_code=400, detail="Invalid credentials")


@app.post("/notices/{notice_id}/claim")
def claim_notice(notice_id: int, db: Session = Depends(get_db), username: str = Header(...)):
    claimed = crud.claim_notice(db, notice_id, username)
    if claimed is None:
        raise HTTPException(status_code=404, detail="Notice not found")
    if claimed is False:
        raise HTTPException(status_code=400, detail="Item already claimed")
    return {"message": "Item claimed successfully", "claimed_by": username}


@app.get("/claimed", response_model=list[schemas.Notice])
def get_claimed_notices(db: Session = Depends(get_db)):
    return crud.get_claimed_notices(db)
