from fastapi import HTTPException, Response, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.crud.users import UserCRUD
from app.db.db import get_db_session  # Import the session dependency
from app.dependencies.auth import require_role  # Import the get_current_user dependency

router = InferringRouter(prefix="/users", tags=["users"])

@cbv(router)
class UserRoutes:
    def __init__(self, db: AsyncSession = Depends(get_db_session)):
        self.user_crud = UserCRUD(db)

    @router.post("/", response_model=UserOut, status_code=201)
    async def create_user_route(self, user: UserCreate, current_user: dict = Depends(require_role(["admin", "resident"]))):
        try:
            if current_user is not True:
                raise HTTPException(status_code=403, detail="Not authorized to create a user")
            new_user_data = await self.user_crud.create_user(user)
            return new_user_data
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.get("/{user_id}", response_model=UserOut, status_code=200)
    async def get_user_by_id(self, user_id: int, current_user: dict = Depends(require_role(["admin", "resident"]))):
        try:
            if current_user is not True:
                raise HTTPException(status_code=403, detail="Not authorized to access this user")
            user_data = await self.user_crud.get_user(user_id)
            if not user_data:
                raise HTTPException(status_code=404, detail="User not found")
            return user_data
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.get("/usersbycondo/{condo_id}", response_model=list[UserOut], status_code=200)
    async def get_users_by_condo_route(self, condo_id: int, current_user: dict = Depends(require_role(["admin", "resident"]))):
        try:
            if current_user is not True:
                raise HTTPException(status_code=403, detail="Not authorized to access users in this condo")
            users_data = await self.user_crud.get_users_by_condo(condo_id)
            if not users_data:
                raise HTTPException(status_code=404, detail="Users not found for this condo")
            return users_data
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.get("/", response_model=list[UserOut], status_code=200)
    async def get_all_users(self, current_user: dict = Depends(require_role(["admin", "resident"]))):
        try:
            if current_user is None:
                raise HTTPException(status_code=403, detail="Not authorized to access all users")
            users_data = await self.user_crud.get_all_users()
            return users_data
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.put("/{user_id}", response_model=UserOut, status_code=200)
    async def update_user_route(self, user_id: int, user: UserUpdate, current_user: dict = Depends(require_role(["admin", "resident"]))):
        try:
            if current_user is not True:
                raise HTTPException(status_code=403, detail="Not authorized to update this user")
            updated_user_data = await self.user_crud.update_user(user_id, user)
            return updated_user_data
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.delete("/{user_id}")
    async def delete_user_route(self, user_id: int, current_user: dict = Depends(require_role(["admin", "resident"]))):
        try:
            if current_user is not True:
                raise HTTPException(status_code=403, detail="Not authorized to delete this user")
            await self.user_crud.delete_user(user_id)
            return Response(status_code=204)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
