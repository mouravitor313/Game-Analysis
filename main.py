import pandas as pd
from fastapi import FastAPI, HTTPException, Depends
from typing import List, Annotated
import models
from database import engine, get_db
from sqlalchemy.orm import Session
from routes import user_routes, games_routes, sonic_routes

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
db_depedency = Annotated[Session, Depends(get_db)]

app.include_router(user_routes.router, prefix="/users", tags=["users"])
app.include_router(games_routes.router, prefix="/games", tags=["games"])
app.include_router(sonic_routes.router, prefix="/chat", tags=["chat"])