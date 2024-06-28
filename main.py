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
app.include_router(sonic_routes.router, prefix="/chat", tags=["chat"])

@app.middleware("http")
async def add_token_refresh_middleware(request: Request, call_next):
    response = await call_next(request)

    if response.status_code == 401 and 'Not authenticated' in response.body.decode():
        auth_jwt = AuthJWT(request)
        try:
            auth_jwt.jwt_refresh_token_required()
            new_access_token = auth_jwt.create_access_token(subject=auth_jwt.get_jwt_subject())
            response = JSONResponse(content={"access_token": new_access_token})
        except Exception:
            pass

    return response