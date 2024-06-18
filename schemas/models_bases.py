from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    password: str

class GameBase(BaseModel):
    name: str
    genre: str
    completed: bool
    user_id: int

class TokenBase(BaseModel):
    acess_token: str
    token_type: str