from fastapi import APIRouter, HTTPException, Depends
from models import User
from database import db_depedency
from schemas.models_bases import UserBase, TokenBase
from fastapi_jwt_auth import AuthJWT

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

@router.post("/login", response_model=TokenBase)
async def login(user: UserBase, db: db_depedency, Authorize: AuthJWT = Depends()):
    user_query = db.query(User).filter(User.username == user.username).first()

    if not user_query or not user_query.check_password(user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    access_token = Authorize.create_access_token(subject=user.username)
    refresh_token = Authorize.create_refresh_token(subject=user.username)
    user_query.refresh_token = refresh_token
    
    db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh", response_model=TokenBase)
async def refresh(Authorize: AuthJWT = Depends(), db: db_depedency = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Refresh token is invalid")

    current_user = Authorize.get_jwt_subject()
    user_query = db.query(User).filter(User.username == current_user).first()

    if not user_query or user_query.refresh_token != Authorize._token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token, "refresh_token": Authorize._token, "token_type": "bearer"}