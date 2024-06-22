import pandas as pd
from assistent.sonic_assistant import Sonic
from assistent.sonic_prompts import prompts_sonic
from fastapi import FastAPI, HTTPException, Depends
from typing import List, Annotated
import models
from database import engine, get_db
from sqlalchemy.orm import Session
from routes import user_routes, games_routes
from config import settings

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
db_depedency = Annotated[Session, Depends(get_db)]

app.include_router(user_routes.router, prefix="/user", tags=["user"])
app.include_router(games_routes.router, prefix="/games", tags=["games"])
