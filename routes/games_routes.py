from fastapi import APIRouter, HTTPException, Depends
from models import Game
from database import db_depedency
from schemas.models_bases import GameBase
from fastapi_jwt_auth import AuthJWT
from .user_routes import get_current_user

router = APIRouter()

def get_game(current_user_id: int, db: db_depedency, Authorize: AuthJWT = Depends()):
    result = db.query(Game).filter(Game.user_id == current_user_id).all()
    if not result:
        raise HTTPException(status_code=400, detail='Games not found!')
    return [game.to_dict() for game in result]

@router.post("/insert-game")
async def insert_game(game: GameBase, db: db_depedency, Authorize: AuthJWT = Depends()):
    current_user = get_current_user(db, Authorize)
    
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated!")
        
    new_game = Game(
        name = game.name,
        platform = game.platform,
        completed = game.completed,
        complete_time = game.complete_time,
        user_id = current_user.id
    )
     
    db.add(new_game)
    db.commit()
    return {"message": "Game inserted!"}

@router.get("/get-game")
async def get_game_endpoint(db: db_depedency, Authorize: AuthJWT = Depends()):
    current_user = get_current_user(db, Authorize)

    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated!")
    
    result = get_game(current_user.id, db, Authorize)
    return result

    
    
    
    