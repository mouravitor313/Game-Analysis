from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    password: str
    is_active: str
    role: str

class GameBase(BaseModel):
    name: str
    platform: str
    completed: bool
    complete_time: int
    user_id: int

class ChatRequest(BaseModel):
    message: str

class TokenBase(BaseModel):
    acess_token: str
    token_type: str