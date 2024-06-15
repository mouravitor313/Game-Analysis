import pandas as pd
from src.assistants.mario_assistant import Mario
from src.prompts.mario_prompts import prompts_mario
from src.assistants.sonic_assistant import Sonic
from src.prompts.sonic_prompts import prompts_sonic
from fastapi import FastAPI, HTTPException, Depends
from typing import List, Annotated
import models
from database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from routes import user_routes

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
db_depedency = Annotated[Session, Depends(get_db)]

app.include_router(user_routes.router)
