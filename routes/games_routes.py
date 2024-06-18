from fastapi import APIRouter, HTTPException, Depends
from models import Game
from database import db_depedency
from schemas.models_bases import GameBase
from fastapi_jwt_auth import AuthJWT
from .user_routes import get_current_user

router = APIRouter()

@router.post("/insert-game")
async def insert_game(game: GameBase, db: db_depedency, Authorize: AuthJWT = Depends()):
    current_user = get_current_user(db, Authorize)
    
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated!")
        
    new_game = Game(
        name=game.name,
        genre=game.genre,
        completed=game.completed,
        user_id=current_user.id
    )
    
    db.add(new_game)
    db.commit()
    return {"message": "Game inserted!"}

@router.get("/get-game")
async def get_game(db: db_depedency, Authorize: AuthJWT = Depends()):
    current_user = get_current_user(db, Authorize)

    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated!")
    result = db.query(Game).filter(Game.user_id == current_user.id).all()
    
    if not result:
        raise HTTPException(status_code=400, detail='Games not found!')
    return result
    