from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from typing import List

from app.models.condo import Condo  # Assuming you have the Condo model
from app.schemas.condo import CondoCreate, CondoUpdate, CondoOut
from app.utils.logger import logger  # Import the logger


class CondosCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_condo(self, condo: CondoCreate) -> CondoOut:
        try:
            logger.debug(f"Creating condo with data: {condo}")
            new_condo = Condo(
                name=condo.name,
                address=condo.address,
            )
            self.db.add(new_condo)
            await self.db.commit()
            await self.db.refresh(new_condo)
            logger.info(f"Condo created successfully: {new_condo}")
            return CondoOut.model_validate(new_condo)  # Use model_validate for output
        except Exception as e:
            logger.error(f"Error creating condo: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error creating condo: {str(e)}")

    async def get_condo_by_id(self, condo_id: int) -> CondoOut:
        try:
            logger.debug(f"Fetching condo with ID: {condo_id}")
            query = select(Condo).where(Condo.id == condo_id)
            result = await self.db.execute(query)
            condo = result.scalars().first()
            if not condo:
                logger.warning(f"Condo not found with ID: {condo_id}")
                raise HTTPException(status_code=404, detail="Condo not found")
            logger.info(f"Condo fetched successfully: {condo}")
            return CondoOut.model_validate(condo)  # Use model_validate for output
        except Exception as e:
            logger.error(f"Error fetching condo: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error fetching condo: {str(e)}")

    async def get_all_condos(self) -> List[CondoOut]:
        try:
            logger.debug("Fetching all condos")
            query = select(Condo)
            result = await self.db.execute(query)
            condos = result.scalars().all()
            logger.info(f"Fetched {len(condos)} condos")
            return [CondoOut.model_validate(c) for c in condos]
        except Exception as e:
            logger.error(f"Error fetching condos: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error fetching condos: {str(e)}")

    async def update_condo(self, condo_id: int, condo_data: CondoUpdate) -> CondoOut:
        try:
            logger.debug(f"Updating condo with ID: {condo_id} and data: {condo_data}")
            query = select(Condo).where(Condo.id == condo_id)
            result = await self.db.execute(query)
            condo = result.scalars().first()

            if not condo:
                logger.warning(f"Condo not found with ID: {condo_id}")
                raise HTTPException(status_code=404, detail="Condo not found")

            # Update the condo fields
            condo.name = condo_data.name
            condo.address = condo_data.address

            # Commit the changes to the database
            await self.db.commit()
            await self.db.refresh(condo)
            logger.info(f"Condo updated successfully: {condo}")
            return CondoOut.model_validate(condo)  # Use model_validate for output

        except Exception as e:
            logger.error(f"Error updating condo: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error updating condo: {str(e)}")

    async def delete_condo(self, condo_id: int):
        try:
            logger.debug(f"Deleting condo with ID: {condo_id}")
            query = select(Condo).where(Condo.id == condo_id)
            result = await self.db.execute(query)
            condo = result.scalars().first()

            if not condo:
                logger.warning(f"Condo not found with ID: {condo_id}")
                raise HTTPException(status_code=404, detail="Condo not found")

            # Delete the condo
            await self.db.delete(condo)
            await self.db.commit()
            logger.info(f"Condo deleted successfully with ID: {condo_id}")
            return CondoOut.model_validate(condo)  # Optionally return the deleted condo for confirmation
        except Exception as e:
            logger.error(f"Error deleting condo: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error deleting condo: {str(e)}")
