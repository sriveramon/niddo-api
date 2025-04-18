from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.utils.jwt import verify_token
from app.utils.logger import logger  # Import the logger
import os

ENVIROMENT = os.getenv("ENV")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        logger.debug("Attempting to verify token")
        if ENVIROMENT == "DeVeLoPmEnT":
            logger.info("Development environment detected, skipping token verification")
            return True

        credentials = verify_token(token)
        if credentials is None:
            logger.warning("Invalid token provided")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        logger.info(f"Token verified successfully for user ID: {credentials.get('user_id')}")
        return credentials  
    except Exception as e:
        logger.error(f"Error verifying token: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Token verification failed")

def require_role(required_roles: list[str]):
    async def role_checker(current_user: dict = Depends(get_current_user)):
        try:
            logger.debug(f"Checking roles for user: {current_user.get('user_id')}")
            if current_user["user_role"] not in required_roles:
                logger.warning(f"Access denied for user ID: {current_user.get('user_id')} with role: {current_user['role']}")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You don't have access to this resource"
                )
            logger.info(f"Role check passed for user ID: {current_user.get('user_id')}")
            return current_user
        except Exception as e:
            logger.error(f"Error during role check: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Role verification failed")
    return role_checker