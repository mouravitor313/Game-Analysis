from fastapi import APIRouter, HTTPException, Depends
from models import Game
from database import db_depedency
from schemas.models_bases import GameBase, ChatRequest
from fastapi_jwt_auth import AuthJWT
from .user_routes import get_current_user
from .games_routes import get_game
import openai
import pandas as pd
import os

# get my api key and give this value to openai.api_key
API_KEY = os.getenv("API_KEY_OPENAI")
openai.api_key = API_KEY

# open and read the archive with prompt
with open('./prompt.txt', 'r') as content:
    prompt = content.read()

chat_sessions = {}

def chat_with_sonic(user_id, user_message, games: GameBase):
    # list to stores messages
    if user_id not in chat_sessions:
        chat_sessions[user_id]=[
                {"role": "system", "content": prompt + '\n\n' + games}
            ]
    
    chat_sessions[user_id].append({{"role": "user", "content": user_message}})
        
    completions = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=chat_sessions[user_id],
        temperature=0.5,
    )

    message_received_from_model = completions.choices[0].message.content
    chat_sessions[user_id].append({"role": "assistant", "content": message_received_from_model})

    return message_received_from_model

router = APIRouter()

@router.post("/sonic-chat")
def chat_with_sonic_route(chat_request: ChatRequest, db: db_depedency, Authorize: AuthJWT = Depends()):

    games = get_game(db, Authorize)
    current_user = get_current_user(db, Authorize)

    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated!")
    
    user_id = current_user.id
    user_message = chat_request.message
    
    sonic_response = chat_with_sonic(user_id, user_message, games)

    return {"response": sonic_response}

