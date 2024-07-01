from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT
import os

SSH_KEY = os.getenv("SSH_KEY")

class Settings(BaseModel):
    authjwt_secret_key: str = SSH_KEY
    authjwt_token_location: set = {"cookies"}
    authjwt_coockie_secure: bool = False
    authjwt_cookie_csrf_protection: bool = True
    authjwt_coockie_samesite: str = 'lax'

settings = Settings()

@AuthJWT.load_config
def get_config():
    return settings
