from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    password: str

class GamesBase(BaseModel):
    name: str
    genre: str
    completed: bool