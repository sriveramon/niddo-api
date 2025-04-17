from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.user import User
from app.schemas.user import UserOut
from app.schemas.auth import LoginRequest
from typing import List
from app.utils.logger import logger  # Import the logger

class AuthCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def check_login(self, request: LoginRequest) -> UserOut:
        try:
            result = await self.db.execute(select(User).where(User.email == request.email))
            user = result.scalars().first()
            return user
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")
