from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    password: str
    rule: str
    is_active: bool

class GameBase(BaseModel):
    name: str
    platform: str
    completed: bool
    complete_time: float
    user_id: int

class ChatRequest(BaseModel):
    message: str

class TokenBase(BaseModel):
    acess_token: str
    refresh_token: str
    token_type: str