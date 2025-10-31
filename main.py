# main.py
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "CampusBoard API running 🚀"}


# --- Notices ---
@app.get("/notices", response_model=list[schemas.Notice])
def read_notices(db: Session = Depends(get_db)):
    return crud.get_notices(db)


@app.post("/notices", response_model=schemas.Notice)
def create_notice(
    notice: schemas.NoticeCreate,
    username: str = Header(...),  # require username header for admin check
    db: Session = Depends(get_db),
):
    """
    Require an authenticated username header and only allow admin users to create notices.
    Frontend sends 'username' header (from localStorage).
    """
    # Accept the special hardcoded admin login, or verify in DB for other users
    if username == "admin":
        # hardcoded admin allowed
        pass
    else:
        user = crud.get_user_by_username(db, username)
        if not user or getattr(user, "role", None) != "admin":
            raise HTTPException(status_code=403, detail="Only admin can create notices")

    return crud.create_notice(db, notice)


@app.delete("/notices/{notice_id}")
def delete_notice(notice_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_notice(db, notice_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Notice not found")
    return {"message": "Deleted successfully"}


@app.post("/notices/{notice_id}/claim")
def request_claim_endpoint(notice_id: int, db: Session = Depends(get_db), username: str = Header(...)):
    """
    User requests to claim a lost item. This creates a pending claim (under review).
    """
    res = crud.request_claim(db, notice_id, username)
    if res is None:
        raise HTTPException(status_code=404, detail="Notice not found")
    if res is False:
        raise HTTPException(status_code=400, detail="Item already claimed")
    if res == "conflict":
        raise HTTPException(status_code=400, detail="There is already a pending claim for this item")
    return {"message": "Claim submitted and is under review"}


@app.get("/claimed", response_model=list[schemas.Notice])
def get_claimed_notices(db: Session = Depends(get_db)):
    return crud.get_claimed_notices(db)


# --- Claims review endpoints (Admin only) ---
@app.get("/claims", response_model=list[schemas.Notice])
def get_pending_claims(db: Session = Depends(get_db), username: str = Header(...)):
    # require admin
    if username != "admin":
        user = crud.get_user_by_username(db, username)
        if not user or getattr(user, "role", None) != "admin":
            raise HTTPException(status_code=403, detail="Only admin can review claims")
    return crud.get_pending_claims(db)


@app.post("/claims/{notice_id}/approve")
def approve_claim_endpoint(notice_id: int, db: Session = Depends(get_db), username: str = Header(...)):
    if username != "admin":
        user = crud.get_user_by_username(db, username)
        if not user or getattr(user, "role", None) != "admin":
            raise HTTPException(status_code=403, detail="Only admin can approve claims")
    res = crud.approve_claim(db, notice_id)
    if res is None:
        raise HTTPException(status_code=404, detail="Notice not found")
    if res is False:
        raise HTTPException(status_code=400, detail="Notice is not pending or cannot be approved")
    return {"message": "Claim approved", "claimed_by": res.claimed_by}


@app.post("/claims/{notice_id}/reject")
def reject_claim_endpoint(notice_id: int, db: Session = Depends(get_db), username: str = Header(...)):
    if username != "admin":
        user = crud.get_user_by_username(db, username)
        if not user or getattr(user, "role", None) != "admin":
            raise HTTPException(status_code=403, detail="Only admin can reject claims")
    res = crud.reject_claim(db, notice_id)
    if res is None:
        raise HTTPException(status_code=404, detail="Notice not found")
    if res is False:
        raise HTTPException(status_code=400, detail="Notice is not pending or cannot be rejected")
    return {"message": "Claim rejected"}


# --- Auth ---
@app.post("/signup", response_model=schemas.UserOut)
def signup(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    username = payload.username.strip()
    if username.lower() == "admin":
        raise HTTPException(status_code=400, detail="'admin' username is reserved")

    existing = crud.get_user_by_username(db, username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    user = crud.create_user(db, username=username, password=payload.password, role="user")
    return schemas.UserOut(username=user.username, role=user.role)


@app.post("/login", response_model=schemas.UserOut)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    # Hardcoded admin override
    if payload.username == "admin" and payload.password == "admin123":
        return schemas.UserOut(username="admin", role="admin")

    user = crud.get_user_by_username(db, payload.username)
    if not user or not crud.verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return schemas.UserOut(username=user.username, role=user.role)
