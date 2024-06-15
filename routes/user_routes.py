from fastapi import APIRouter, HTTPException, Depends
from models import User
from database import SessionLocal, get_db
from sqlalchemy.orm import Session
from schemas import UserBase

router = APIRouter()

@router.post("/register")
async def register(user: UserBase, db: Session = Depends(get_db)):
    user_query = db.query(User).filter(User.username == user.username).first()
    if user_query:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = User(username=user.username)
    new_user.set_password(user.password)
    db.add(new_user)
    db.commit()
    return {"message": "User created"}

@router.post("/login")
async def login(user: UserBase, db: Session = Depends(get_db)):
    user_query = db.query(User).filter(User.username == user.username).first()
    if not user_query or not user_query.check_password(user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"message": "Logged in"}