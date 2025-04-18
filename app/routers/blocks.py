from fastapi import HTTPException, Depends, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.block import BlockCreate, BlockOut, BlockUpdate
from app.crud.blocks import BlockCRUD
from app.db.db import get_db_session
from app.dependencies.auth import require_role

router = InferringRouter(prefix="/blocks", tags=["blocks"])

@cbv(router)
class BlockRoutes:
    def __init__(self, db: AsyncSession = Depends(get_db_session)):
        self.block_crud = BlockCRUD(db)

    @router.post("/", response_model=BlockOut, status_code=201)
    async def create_block(self, block: BlockCreate, current_user: dict = Depends(require_role(["admin", "resident"]))):
        try:
            if current_user is False:
                raise HTTPException(status_code=403, detail="Not authorized to create a block")
            created_block = await self.block_crud.create_block(block)
            return created_block
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.get("/blocksbyamenity/{amenity_id}", response_model=List[BlockOut], status_code=200)
    async def get_blocks_by_amenity(self, amenity_id: int, current_user: dict = Depends(require_role(["admin", "resident"]))):
        try:
            if current_user is False:
                raise HTTPException(status_code=403, detail="Not authorized to view blocks")
            blocks_data = await self.block_crud.get_blocks_by_amenity(amenity_id)
            if not blocks_data:
                raise HTTPException(status_code=404, detail="No blocks found for this amenity")
            return blocks_data
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.get("/{block_id}", response_model=BlockOut, status_code=200)
    async def get_block_by_id(self, block_id: int, current_user: dict = Depends(require_role(["admin", "resident"]))):
        try:
            if current_user is False:
                raise HTTPException(status_code=403, detail="Not authorized to view this block")
            block_data = await self.block_crud.get_block_by_id(block_id)
            if not block_data:
                raise HTTPException(status_code=404, detail="Block not found")
            return block_data
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.put("/{block_id}", response_model=BlockOut, status_code=200)
    async def update_block(self, block_id: int, block: BlockUpdate, current_user: dict = Depends(require_role(["admin", "resident"]))):
        try:
            if current_user is False:
                raise HTTPException(status_code=403, detail="Not authorized to update this block")
            updated_block = await self.block_crud.update_block(block_id, block)
            return updated_block
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.delete("/{block_id}")
    async def delete_block(self, block_id: int, current_user: dict = Depends(require_role(["admin", "resident"]))):
        try:
            if current_user is False:
                raise HTTPException(status_code=403, detail="Not authorized to delete this block")
            await self.block_crud.delete_block(block_id)
            return Response(status_code=204)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
