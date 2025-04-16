from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from typing import List

from app.models.amenity import Amenity
from app.schemas.amenity import AmenityCreate, AmenityUpdate, AmenityOut


class AmenityCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_amenity(self, amenity: AmenityCreate) -> AmenityOut:
        try:
            new_amenity = Amenity(
                name=amenity.name,
                description=amenity.description,
                start_time=amenity.start_time,
                end_time=amenity.end_time,
                condo_id=amenity.condo_id,
            )
            self.db.add(new_amenity)
            await self.db.commit()
            await self.db.refresh(new_amenity)
            # Use model_validate() instead of from_orm()
            return AmenityOut.model_validate(new_amenity)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating amenity: {str(e)}")

    async def get_amenity_by_id(self, amenity_id: int) -> AmenityOut:
        try:
            query = select(Amenity).where(Amenity.id == amenity_id)
            result = await self.db.execute(query)
            amenity = result.scalars().first()
            if not amenity:
                raise HTTPException(status_code=404, detail="Amenity not found")
            return AmenityOut.model_validate(amenity)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching amenity: {str(e)}")

    async def get_all_amenities_by_condo(self, condo_id: int) -> List[AmenityOut]:
        try:
            query = select(Amenity).where(Amenity.condo_id == condo_id)
            result = await self.db.execute(query)
            amenities = result.scalars().all()
            return [AmenityOut.model_validate(a) for a in amenities]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching amenities: {str(e)}")

    async def update_amenity(self, amenity_id: int, amenity_data: AmenityUpdate) -> AmenityOut:
        try:
            query = select(Amenity).where(Amenity.id == amenity_id)
            result = await self.db.execute(query)
            amenity = result.scalars().first()
            
            if not amenity:
                raise HTTPException(status_code=404, detail="Amenity not found")

            # Update the amenity fields
            amenity.name = amenity_data.name
            amenity.description = amenity_data.description
            amenity.start_time = amenity_data.start_time
            amenity.end_time = amenity_data.end_time

            # Commit the changes to the database
            await self.db.commit()
            await self.db.refresh(amenity)

            # Validate and return the updated amenity
            return AmenityOut.model_validate(amenity)  # Use model_validate to validate the output

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating amenity: {str(e)}")

    async def delete_amenity(self, amenity_id: int):
        try:
            query = select(Amenity).where(Amenity.id == amenity_id)
            result = await self.db.execute(query)
            amenity = result.scalars().first()
            
            if not amenity:
                raise HTTPException(status_code=404, detail="Amenity not found")

            # Delete the amenity
            await self.db.delete(amenity)
            await self.db.commit()

            # Optionally return some confirmation (since deletion doesn't return data, this is just a model validation for the confirmation)
            # Example: Returning a deleted amenity or a confirmation message
            return AmenityOut.model_validate(amenity)# This ensures the returned data is validated

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting amenity: {str(e)}")

