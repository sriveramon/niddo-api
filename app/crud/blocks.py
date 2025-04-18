from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from typing import List
from sqlalchemy.orm import joinedload
from app.models.block import Block
from app.schemas.block import BlockCreate, BlockUpdate, BlockOut
from app.utils.logger import logger


class BlockCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_block(self, block: BlockCreate) -> BlockOut:
        try:
            logger.debug(f"Creating block with data: {block}")
            new_block = Block(
                amenity_id=block.amenity_id,
                start_date=block.start_date,
                end_date=block.end_date,
                start_time=block.start_time,
                end_time=block.end_time,
                reason=block.reason,
            )
            self.db.add(new_block)
            await self.db.commit()
            await self.db.refresh(new_block)
            logger.info(f"Block created successfully: {new_block}")
            return BlockOut.model_validate(new_block)
        except Exception as e:
            logger.error(f"Error creating block: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error creating block: {str(e)}")

    async def get_block_by_id(self, block_id: int) -> BlockOut:
        try:
            logger.debug(f"Fetching block with ID: {block_id}")
            query = select(Block).where(Block.id == block_id)
            result = await self.db.execute(query)
            block = result.scalars().first()
            if not block:
                logger.warning(f"Block not found with ID: {block_id}")
                raise HTTPException(status_code=404, detail="Block not found")
            logger.info(f"Block fetched successfully: {block}")
            return BlockOut.model_validate(block)
        except Exception as e:
            logger.error(f"Error fetching block: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error fetching block: {str(e)}")

    async def get_blocks_by_amenity(self, amenity_id: int) -> List[BlockOut]:
        try:
            logger.debug(f"Fetching all blocks for amenity ID: {amenity_id}")
            query = (
                select(Block)
                .options(joinedload(Block.amenity))
                .where(Block.amenity_id == amenity_id)
            )
            result = await self.db.execute(query)
            blocks = result.scalars().all()

            logger.info(f"Fetched {len(blocks)} blocks for amenity ID: {amenity_id}")
            return [
                BlockOut(
                    id=block.id,
                    amenity_name=block.amenity.name,
                    start_date=block.start_date,
                    end_date=block.end_date,
                    start_time=block.start_time,
                    end_time=block.end_time,
                    reason=block.reason,
                )
                for block in blocks
            ]
        except Exception as e:
            logger.error(f"Error fetching blocks: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error fetching blocks: {str(e)}")

    async def update_block(self, block_id: int, block_data: BlockUpdate) -> BlockOut:
        try:
            logger.debug(f"Updating block with ID: {block_id} and data: {block_data}")
            query = select(Block).where(Block.id == block_id)
            result = await self.db.execute(query)
            block = result.scalars().first()

            if not block:
                logger.warning(f"Block not found with ID: {block_id}")
                raise HTTPException(status_code=404, detail="Block not found")

            block.amenity_id = block_data.amenity_id
            block.start_date = block_data.start_date
            block.end_date = block_data.end_date
            block.start_time = block_data.start_time
            block.end_time = block_data.end_time
            block.reason = block_data.reason

            await self.db.commit()
            await self.db.refresh(block)
            logger.info(f"Block updated successfully: {block}")
            return BlockOut.model_validate(block)
        except Exception as e:
            logger.error(f"Error updating block: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error updating block: {str(e)}")

    async def delete_block(self, block_id: int):
        try:
            logger.debug(f"Deleting block with ID: {block_id}")
            query = select(Block).where(Block.id == block_id)
            result = await self.db.execute(query)
            block = result.scalars().first()

            if not block:
                logger.warning(f"Block not found with ID: {block_id}")
                raise HTTPException(status_code=404, detail="Block not found")

            await self.db.delete(block)
            await self.db.commit()
            logger.info(f"Block deleted successfully with ID: {block_id}")
            return BlockOut.model_validate(block)
        except Exception as e:
            logger.error(f"Error deleting block: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error deleting block: {str(e)}")
