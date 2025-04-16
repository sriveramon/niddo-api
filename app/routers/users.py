from fastapi import HTTPException, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.crud.users import UserCRUD
import json

router = InferringRouter(prefix="/users", tags=["users"])
@cbv(router)
class UserRoutes:
    def __init__(self):
        self.user_crud = UserCRUD()

    @router.post("/", response_model=UserOut, )
    async def create_user_route(self, user: UserCreate):
        try:
            self.user_crud.create_user(user)
            user_json = json.dumps(UserOut(**user.model_dump()).model_dump())
            return Response(content=user_json, status_code=201)  # Created

        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.get("/{user_id}", response_model=UserOut)
    async def get_user_route(self, user_id: int):
        try:
            user = self.user_crud.get_user(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            user_json = json.dumps(user.model_dump())
            return Response(content=user_json, status_code=200)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        
    @router.get("/usersbycondo/{condo_id}", response_model=list[UserOut])
    async def get_users_by_condo_route(self, condo_id: int):
        try:
            users_data = self.user_crud.get_users_by_condo(condo_id)
            if not users_data:
                raise HTTPException(status_code=404, detail="Users not found for this condo")
            users_json = json.dumps([user.model_dump() for user in users_data])
            return Response(content=users_json, status_code=200)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.get("/", response_model=list[UserOut])
    async def get_all_users_route(self):
        try:
            data = self.user_crud.get_all_users()
            users_json = json.dumps([user.model_dump() for user in data])
            return Response(content=users_json, status_code=200)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        
    @router.delete("/{user_id}")
    async def delete_user_route(self, user_id: int):
        try:
            self.user_crud.delete_user(user_id)
            return Response(status_code=204)  
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)