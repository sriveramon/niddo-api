from fastapi import HTTPException, Depends, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.amenity import AmenityCreate, AmenityOut, AmenityUpdate
from app.crud.amenities import AmenityCRUD
from app.db.db import get_db_session

router = InferringRouter(prefix="/amenities", tags=["amenities"])

@cbv(router)
class AmenitysRoutes:
    def __init__(self, db: AsyncSession = Depends(get_db_session)):
        self.amenity_crud = AmenityCRUD(db)

    @router.post("/", response_model=AmenityOut, status_code=201)
    async def create_amenity(self, amenity: AmenityCreate):
        try:
            created_amenity = await self.amenity_crud.create_amenity(amenity)
            return created_amenity
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.get("/amenitiesbycondo/{condo_id}", response_model=List[AmenityOut], status_code=200)
    async def get_amenities_by_condo(self, condo_id: int):
        try:
            amenities_data = await self.amenity_crud.get_all_amenities_by_condo(condo_id)
            if not amenities_data:
                raise HTTPException(status_code=404, detail="Amenities not found for this condo")
            return amenities_data
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.get("/{amenity_id}", response_model=AmenityOut, status_code=200)
    async def get_amenity_by_id(self, amenity_id: int):
        try:
            amenity_data = await self.amenity_crud.get_amenity_by_id(amenity_id)
            if not amenity_data:
                raise HTTPException(status_code=404, detail="Amenity not found")
            return amenity_data
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.put("/{amenity_id}", response_model=AmenityOut, status_code=200)
    async def update_amenity(self, amenity_id: int, amenity: AmenityUpdate):
        try:
            updated_amenity = await self.amenity_crud.update_amenity(amenity_id, amenity)
            return updated_amenity
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        
    @router.delete("/{amenity_id}")
    async def delete_user_route(self, amenity_id: int):
        try:
            await self.amenity_crud.delete_amenity(amenity_id)
            return Response(status_code=204)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
