from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from typing import List
from app.models.visitor import Visitor
from app.schemas.visitor import VisitorCreate, VisitorUpdate, VisitorOut
from app.utils.logger import logger


class VisitorsCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_visitor(self, visitor: VisitorCreate) -> VisitorOut:
        try:
            logger.debug(f"Creating visitor with data: {visitor}")
            new_visitor = Visitor(
                identification=visitor.identification,
                user_id=visitor.user_id,
                condo_id=visitor.condo_id,
                plate=visitor.plate,
                visit_date=visitor.visit_date,
                status=visitor.status,
                unit_number=visitor.unit_number,
                visit_name=visitor.visit_name  # ✅ Added field
            )
            self.db.add(new_visitor)
            await self.db.commit()
            await self.db.refresh(new_visitor)
            logger.info(f"Visitor created successfully: {new_visitor}")
            return VisitorOut.model_validate(new_visitor)
        except Exception as e:
            logger.error(f"Error creating visitor: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error creating visitor: {str(e)}")

    async def get_visitor_by_id(self, visitor_id: int) -> VisitorOut:
        try:
            logger.debug(f"Fetching visitor with ID: {visitor_id}")
            query = select(Visitor).where(Visitor.id == visitor_id)
            result = await self.db.execute(query)
            visitor = result.scalars().first()

            if not visitor:
                logger.warning(f"Visitor not found with ID: {visitor_id}")
                raise HTTPException(status_code=404, detail="Visitor not found")

            logger.info(f"Visitor fetched successfully: {visitor}")
            return VisitorOut.model_validate(visitor)
        except Exception as e:
            logger.error(f"Error fetching visitor: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error fetching visitor: {str(e)}")

    async def get_visitors_by_user(self, user_id: int) -> List[VisitorOut]:
        try:
            logger.debug(f"Fetching visitors for user ID: {user_id}")
            query = select(Visitor).where(Visitor.user_id == user_id)
            result = await self.db.execute(query)
            visitors = result.scalars().all()

            logger.info(f"Fetched {len(visitors)} visitors for user ID: {user_id}")
            return [VisitorOut.model_validate(v) for v in visitors]
        except Exception as e:
            logger.error(f"Error fetching visitors: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error fetching visitors: {str(e)}")

    async def get_visitors_by_condo(self, condo_id: int) -> List[VisitorOut]:
        try:
            logger.debug(f"Fetching visitors for condo ID: {condo_id}")
            query = select(Visitor).where(Visitor.condo_id == condo_id)
            result = await self.db.execute(query)
            visitors = result.scalars().all()

            logger.info(f"Fetched {len(visitors)} visitors for condo ID: {condo_id}")
            return [VisitorOut.model_validate(v) for v in visitors]
        except Exception as e:
            logger.error(f"Error fetching visitors by condo: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error fetching visitors by condo: {str(e)}")

    async def update_visitor(self, visitor_id: int, data: VisitorUpdate) -> VisitorOut:
        try:
            logger.debug(f"Updating visitor with ID: {visitor_id} and data: {data}")
            query = select(Visitor).where(Visitor.id == visitor_id)
            result = await self.db.execute(query)
            visitor = result.scalars().first()

            if not visitor:
                logger.warning(f"Visitor not found with ID: {visitor_id}")
                raise HTTPException(status_code=404, detail="Visitor not found")

            visitor.identification = data.identification
            visitor.user_id = data.user_id
            visitor.condo_id = data.condo_id
            visitor.plate = data.plate
            visitor.visit_date = data.visit_date
            visitor.status = data.status
            visitor.unit_number = data.unit_number
            visitor.visit_name = data.visit_name  # ✅ Added field

            await self.db.commit()
            await self.db.refresh(visitor)
            logger.info(f"Visitor updated successfully: {visitor}")
            return VisitorOut.model_validate(visitor)
        except Exception as e:
            logger.error(f"Error updating visitor: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error updating visitor: {str(e)}")

    async def delete_visitor(self, visitor_id: int):
        try:
            logger.debug(f"Deleting visitor with ID: {visitor_id}")
            query = select(Visitor).where(Visitor.id == visitor_id)
            result = await self.db.execute(query)
            visitor = result.scalars().first()

            if not visitor:
                logger.warning(f"Visitor not found with ID: {visitor_id}")
                raise HTTPException(status_code=404, detail="Visitor not found")

            await self.db.delete(visitor)
            await self.db.commit()
            logger.info(f"Visitor deleted successfully with ID: {visitor_id}")
        except Exception as e:
            logger.error(f"Error deleting visitor: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error deleting visitor: {str(e)}")
