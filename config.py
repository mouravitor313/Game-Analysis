from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT
import os

SSH_KEY = os.getenv("SSH_KEY")

class Settings(BaseModel):
    authjwt_secret_key: str = SSH_KEY

settings = Settings()

@AuthJWT.load_config
def get_config():
    return settings
