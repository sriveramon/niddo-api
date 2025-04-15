from fastapi import HTTPException, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from app.schemas.amenitie import AmenitieCreate, AmenitieOut, AmenitieUpdate
from app.crud.amenities import AmenitiesCRUD
import json

router = InferringRouter(prefix="/amenities", tags=["amenities"])
@cbv(router)
class AmenitiesRoutes:
    def __init__(self):
        self.amenitie_crud = AmenitiesCRUD()

    @router.post("/", response_model=AmenitieOut, )
    async def create_user_route(self, amenitie: AmenitieCreate):
        try:
            self.amenitie_crud.create_amenitie(amenitie)
            # Assuming `amenitie` is an object with time attributes
            start_time_str = amenitie.start_time.strftime('%H:%M:%S')
            end_time_str = amenitie.end_time.strftime('%H:%M:%S')

            # Now create a dictionary or model to serialize
            amenitie_json = json.dumps({
                **amenitie.model_dump(),
                'start_time': start_time_str,
                'end_time': end_time_str
            })
            return Response(content=amenitie_json, status_code=201)  # Created

        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    # @router.get("/{user_id}", response_model=UserOut)
    # async def get_user_route(self, user_id: int):
    #     try:
    #         user = self.amenitie_crud.get_user(user_id)
    #         if not user:
    #             raise HTTPException(status_code=404, detail="User not found")
    #         user_json = json.dumps(user.model_dump())
    #         return Response(content=user_json, status_code=200)
    #     except HTTPException as e:
    #         raise HTTPException(status_code=e.status_code, detail=e.detail)

    # @router.get("/", response_model=list[UserOut])
    # async def get_all_users_route(self):
    #     try:
    #         data = self.amenitie_crud.get_all_users()
    #         users_json = json.dumps([user.model_dump() for user in data])
    #         return Response(content=users_json, status_code=200)
    #     except HTTPException as e:
    #         raise HTTPException(status_code=e.status_code, detail=e.detail)
        
    # @router.delete("/{user_id}")
    # async def delete_user_route(self, user_id: int):
    #     try:
    #         self.amenitie_crud.delete_user(user_id)
    #         return Response(status_code=204)  
    #     except HTTPException as e:
    #         raise HTTPException(status_code=e.status_code, detail=e.detail)