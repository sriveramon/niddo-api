from fastapi import HTTPException, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from app.schemas.amenity import AmenityCreate, AmenityOut, AmenityUpdate
from app.crud.amenities import AmenitysCRUD
import json

router = InferringRouter(prefix="/amenities", tags=["amenities"])
@cbv(router)
class AmenitysRoutes:
    def __init__(self):
        self.amenity_crud = AmenitysCRUD()

    @router.post("/", response_model=AmenityOut, )
    async def create_amenitie(self, amenity: AmenityCreate):
        try:
            self.amenity_crud.create_amenitie(amenity)
            # Assuming `amenity` is an object with time attributes
            start_time_str = amenity.start_time.strftime('%H:%M:%S')
            end_time_str = amenity.end_time.strftime('%H:%M:%S')

            # Now create a dictionary or model to serialize
            amenitie_json = json.dumps({
                **amenity.model_dump(),
                'start_time': start_time_str,
                'end_time': end_time_str
            })
            return Response(content=amenitie_json, status_code=201)  # Created

        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.get("/amanetiesbycondo/{condo_id}", response_model=AmenityOut)
    async def get_amenities_by_condo(self, condo_id: int):
        try:
            amenities_data = self.amenity_crud.get_all_amenities_for_condo(condo_id)
            if not amenities_data:
                raise HTTPException(status_code=404, detail="Amenitys not found for this condo")
            amenities_json = json.dumps([amenity.model_dump() for amenity in amenities_data])
            return Response(content=amenities_json, status_code=200)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.get("/{amenitie_id}", response_model=AmenityOut)
    async def get_amenitie_by_id(self, amenitie_id: int):
        try:
            amenitie_data = self.amenity_crud.get_amenitie_by_id(amenitie_id)
            if not amenitie_data:
                raise HTTPException(status_code=404, detail="Amenitys not found for this condo")
            amenitie_json = json.dumps(amenitie_data.model_dump())
            return Response(content=amenitie_json, status_code=200)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        
    @router.put("/{amenitie_id}", response_model=AmenityOut)
    async def update_amenitie(self, amenitie_id: int, amenity: AmenityUpdate):
        try:
            self.amenity_crud.update_amenitie(amenitie_id, amenity)
            # Assuming `amenity` is an object with time attributes
            start_time_str = amenity.start_time.strftime('%H:%M:%S')
            end_time_str = amenity.end_time.strftime('%H:%M:%S')

            # Now create a dictionary or model to serialize
            updated_amenitie_json = json.dumps({
                **amenity.model_dump(),
                'start_time': start_time_str,
                'end_time': end_time_str
            })
            return Response(content=updated_amenitie_json, status_code=200)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    @router.delete("/{amenitie_id}")
    async def delete_amenitie(self, amenitie_id: int):
        try:
            self.amenity_crud.delete_amenitie(amenitie_id)
            return Response(status_code=204)  
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)