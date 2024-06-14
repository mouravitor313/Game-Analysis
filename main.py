import pandas as pd
from src.assistants.mario_assistant import Mario
from src.prompts.mario_prompts import prompts_mario
from src.assistants.sonic_assistant import Sonic
from src.prompts.sonic_prompts import prompts_sonic
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class UserBase(BaseModel):
    username: str
    password: str

class GamesBase(BaseModel):
    name: str
    genre: str
    completed: bool

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_depedency = Annotated[Session, Depends(get_db)]

@app.post("/register")
async def register(user: UserBase, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.username == user.username).first()
    if user_query:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = models.User(username=user.username)
    new_user.set_password(user.password)
    db.add(new_user)
    db.commit()
    return {"message": "User created"}

@app.post("/login")
async def login(user: UserBase, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.username == user.username).first()
    if not user_query or not user_query.check_password(user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"message": "Logged in"}