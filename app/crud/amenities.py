from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from typing import List

from app.models.amenity import Amenity
from app.schemas.amenity import AmenityCreate, AmenityUpdate, AmenityOut
from app.utils.logger import logger  # Import the logger


class AmenityCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_amenity(self, amenity: AmenityCreate) -> AmenityOut:
        try:
            logger.debug(f"Creating amenity with data: {amenity}")
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
            logger.info(f"Amenity created successfully: {new_amenity}")
            return AmenityOut.model_validate(new_amenity)  # Use model_validate for output
        except Exception as e:
            logger.error(f"Error creating amenity: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error creating amenity: {str(e)}")

    async def get_amenity_by_id(self, amenity_id: int) -> AmenityOut:
        try:
            logger.debug(f"Fetching amenity with ID: {amenity_id}")
            query = select(Amenity).where(Amenity.id == amenity_id)
            result = await self.db.execute(query)
            amenity = result.scalars().first()
            if not amenity:
                logger.warning(f"Amenity not found with ID: {amenity_id}")
                raise HTTPException(status_code=404, detail="Amenity not found")
            logger.info(f"Amenity fetched successfully: {amenity}")
            return AmenityOut.model_validate(amenity)
        except Exception as e:
            logger.error(f"Error fetching amenity: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error fetching amenity: {str(e)}")

    async def get_all_amenities_by_condo(self, condo_id: int) -> List[AmenityOut]:
        try:
            logger.debug(f"Fetching all amenities for condo ID: {condo_id}")
            query = select(Amenity).where(Amenity.condo_id == condo_id)
            result = await self.db.execute(query)
            amenities = result.scalars().all()
            logger.info(f"Fetched {len(amenities)} amenities for condo ID: {condo_id}")
            return [AmenityOut.model_validate(a) for a in amenities]
        except Exception as e:
            logger.error(f"Error fetching amenities: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error fetching amenities: {str(e)}")

    async def update_amenity(self, amenity_id: int, amenity_data: AmenityUpdate) -> AmenityOut:
        try:
            logger.debug(f"Updating amenity with ID: {amenity_id} and data: {amenity_data}")
            query = select(Amenity).where(Amenity.id == amenity_id)
            result = await self.db.execute(query)
            amenity = result.scalars().first()

            if not amenity:
                logger.warning(f"Amenity not found with ID: {amenity_id}")
                raise HTTPException(status_code=404, detail="Amenity not found")

            # Update the amenity fields
            amenity.name = amenity_data.name
            amenity.description = amenity_data.description
            amenity.start_time = amenity_data.start_time
            amenity.end_time = amenity_data.end_time

            # Commit the changes to the database
            await self.db.commit()
            await self.db.refresh(amenity)
            logger.info(f"Amenity updated successfully: {amenity}")
            return AmenityOut.model_validate(amenity)  # Use model_validate for output
        except Exception as e:
            logger.error(f"Error updating amenity: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error updating amenity: {str(e)}")

    async def delete_amenity(self, amenity_id: int):
        try:
            logger.debug(f"Deleting amenity with ID: {amenity_id}")
            query = select(Amenity).where(Amenity.id == amenity_id)
            result = await self.db.execute(query)
            amenity = result.scalars().first()

            if not amenity:
                logger.warning(f"Amenity not found with ID: {amenity_id}")
                raise HTTPException(status_code=404, detail="Amenity not found")

            # Delete the amenity
            await self.db.delete(amenity)
            await self.db.commit()
            logger.info(f"Amenity deleted successfully with ID: {amenity_id}")
            return AmenityOut.model_validate(amenity)  # Optionally return the deleted amenity for confirmation
        except Exception as e:
            logger.error(f"Error deleting amenity: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error deleting amenity: {str(e)}")

