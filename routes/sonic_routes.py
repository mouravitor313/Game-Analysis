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

API_KEY = os.getenv("API_KEY_OPENAI")
openai.api_key = API_KEY

with open('routes/prompt.txt', 'r') as content:
    prompt = content.read()

chat_sessions = {}

def chat_with_sonic(user_id, user_message, games):
    if user_id not in chat_sessions:
        chat_sessions[user_id]=[
                {"role": "system", "content": f"{prompt}\n\n{games}"}
            ]
    
    chat_sessions[user_id].append({"role": "user", "content": user_message})
    print(chat_sessions[user_id])    
    completions = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=chat_sessions[user_id],
        temperature=0.8,
    )

    message_received_from_model = completions.choices[0].message.content
    chat_sessions[user_id].append({"role": "assistant", "content": message_received_from_model})

    return message_received_from_model

router = APIRouter()

@router.post("/sonic-chat")
async def chat_with_sonic_route(chat_request: ChatRequest, db: db_depedency, Authorize: AuthJWT = Depends()):

    current_user = get_current_user(db, Authorize)
    games = get_game(current_user.id, db, Authorize)

    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated!")
    
    user_id = current_user.id
    user_message = chat_request.message
    
    sonic_response = chat_with_sonic(user_id, user_message, games)

    return {"response": sonic_response}

