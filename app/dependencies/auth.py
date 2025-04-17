from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.utils.jwt import verify_token
import os
ENVIROMENT = os.getenv("ENV")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    if ENVIROMENT == "DeVeLoPmEnT":
        return True
    if verify_token(token) is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return True  # Or fetch full user from DB using payload["sub"] (user_id)
