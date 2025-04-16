from fastapi import HTTPException, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from app.schemas.amenity import AmenityCreate, AmenityOut, AmenityUpdate
from app.crud.amenities import AmenitysCRUD
from typing import List

router = InferringRouter(prefix="/amenities", tags=["amenities"])
@cbv(router)
class AmenitysRoutes:
    def __init__(self):
        self.amenity_crud = AmenitysCRUD()

    @router.post("/", response_model=AmenityOut, status_code=201)
    async def create_amenitie(self, amenity: AmenityCreate):
        try:
            created_amenity  = self.amenity_crud.create_amenitie(amenity)
            return created_amenity
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.get("/amanetiesbycondo/{condo_id}", response_model=List[AmenityOut], status_code=200)
    async def get_amenities_by_condo(self, condo_id: int):
        try:
            amenities_data = self.amenity_crud.get_all_amenities_by_condo(condo_id)
            if not amenities_data:
                raise HTTPException(status_code=404, detail="Amenitys not found for this condo")
            return amenities_data
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.get("/{amenitie_id}", response_model=AmenityOut, status_code=200)
    async def get_amenitie_by_id(self, amenitie_id: int):
        try:
            amenitie_data = self.amenity_crud.get_amenitie_by_id(amenitie_id)
            if not amenitie_data:
                raise HTTPException(status_code=404, detail="Amenitys not found for this condo")
            return amenitie_data
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        
    @router.put("/{amenitie_id}", response_model=AmenityOut, status_code=200)
    async def update_amenitie(self, amenitie_id: int, amenity: AmenityUpdate):
        try:
            updated_amenitie=self.amenity_crud.update_amenitie(amenitie_id, amenity)
            return updated_amenitie
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    @router.delete("/{amenitie_id}")
    async def delete_amenitie(self, amenitie_id: int):
        try:
            self.amenity_crud.delete_amenitie(amenitie_id)
            return Response(status_code=204)  
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)