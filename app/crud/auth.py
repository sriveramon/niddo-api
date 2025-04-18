from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.user import User
from app.schemas.user import UserOut
from app.schemas.auth import LoginRequest
from app.utils.logger import logger  # Import the logger


class AuthCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def check_login(self, request: LoginRequest) -> UserOut:
        try:
            logger.debug(f"Login attempt for email: {request.email}")
            result = await self.db.execute(select(User).where(User.email == request.email))
            user = result.scalars().first()

            if not user:
                logger.warning(f"Login failed: User not found for email: {request.email}")
                return None

            logger.info(f"User found for email: {request.email}, proceeding with password verification")
            return user
        except Exception as e:
            logger.error(f"Error during login check: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
