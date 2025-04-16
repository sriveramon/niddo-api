from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from typing import List

class UserCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user: UserCreate) -> UserOut:
        try:
            new_user = User(
                name=user.name,
                email=user.email,
                password_hash=user.password,
                condo_id=user.condo_id,
                unit=user.unit
            )
            self.db.add(new_user)
            await self.db.commit()
            await self.db.refresh(new_user)
            return UserOut.model_validate(new_user)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

    async def get_user(self, user_id: int) -> UserOut:
        try:
            result = await self.db.execute(select(User).where(User.id == user_id))
            user_data = result.scalars().first()
            if not user_data:
                raise HTTPException(status_code=404, detail="User not found")
            return UserOut.model_validate(user_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")

    async def get_all_users(self) -> List[UserOut]:
        try:
            result = await self.db.execute(select(User))
            users_data = result.scalars().all()
            return [UserOut.model_validate(user) for user in users_data]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")

    async def get_users_by_condo(self, condo_id: int) -> List[UserOut]:
        try:
            result = await self.db.execute(select(User).filter(User.condo_id == condo_id))
            users_data = result.scalars().all()
            return [UserOut.model_validate(user) for user in users_data]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching users by condo: {str(e)}")

    async def update_user(self, user_id: int, user: UserCreate) -> UserOut:
        try:
            result = await self.db.execute(select(User).filter(User.id == user_id))
            db_user = result.scalars().first()

            if not db_user:
                raise HTTPException(status_code=404, detail="User not found")

            db_user.name = user.name
            db_user.email = user.email
            db_user.password_hash = user.password
            db_user.condo_id = user.condo_id
            db_user.unit = user.unit

            await self.db.commit()
            await self.db.refresh(db_user)
            return UserOut.model_validate(db_user)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")

    async def delete_user(self, user_id: int):
        try:
            result = await self.db.execute(select(User).filter(User.id == user_id))
            db_user = result.scalars().first()

            if not db_user:
                raise HTTPException(status_code=404, detail="User not found")

            await self.db.delete(db_user)
            await self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")
