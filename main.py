from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from typing import List, Annotated
import models
from database import engine, get_db
from sqlalchemy.orm import Session
from routes import user_routes, games_routes, sonic_routes
from config import settings

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
db_depedency = Annotated[Session, Depends(get_db)]

app.include_router(user_routes.router, prefix="/users", tags=["users"])
app.include_router(games_routes.router, prefix="/games", tags=["games"])
app.include_router(games_routes.router, prefix="/chat", tags=["chat"])