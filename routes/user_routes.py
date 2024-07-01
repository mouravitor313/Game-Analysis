from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from models import User
from database import db_depedency
from schemas.models_bases import UserBase, TokenBase


router = APIRouter()

def get_current_user(db: db_depedency, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()

    return db.query(User).filter(User.username == current_user).first()

@router.post("/register")
async def register(user: UserBase, db: db_depedency):
    user_query = db.query(User).filter(User.username == user.username).first()

    if user_query:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    new_user = User(username=user.username)
    new_user.set_password(user.password)

    db.add(new_user)
    db.commit()

    return {"message": "User created"}

@router.post("/login")
async def login(user: UserBase, db: db_depedency, Authorize: AuthJWT = Depends()):
    user_query = db.query(User).filter(User.username == user.username).first()

    if not user_query or not user_query.check_password(user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    access_token = Authorize.create_access_token(subject=user.username)
    refresh_token = Authorize.create_refresh_token(subject=user.username)

    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)

    return {"message": "Successfully login"}

@router.post("/refresh")
async def refresh(db: db_depedency, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Refresh token is invalid")

    current_user = get_current_user(db, Authorize)

    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = Authorize.create_access_token(subject=current_user)
    Authorize.set_access_cookies(new_access_token)
    return {"message": "The token has been refresh"}

@router.delete("/logout")
async def logout(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token is invalid")
    
    Authorize.unset_jwt_cookies()
    return {"msg": "Successfully logout"}