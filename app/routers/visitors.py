from fastapi import HTTPException, Depends, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.visitor import VisitorCreate, VisitorOut, VisitorUpdate
from app.crud.visitors import VisitorsCRUD
from app.db.db import get_db_session
from app.dependencies.auth import require_role  # Import get_current_user dependency

router = InferringRouter(prefix="/visitors", tags=["visitors"])

@cbv(router)
class VisitorsRoutes:
    def __init__(self, db: AsyncSession = Depends(get_db_session)):
        self.visitor_crud = VisitorsCRUD(db)

    @router.post("/", response_model=VisitorOut, status_code=201)
    async def create_visitor(self, visitor: VisitorCreate, current_user: dict = Depends(require_role(["admin", "resident"]))):
        try:
            if current_user is False:
                raise HTTPException(status_code=403, detail="Not authorized to create this visitor")
            created_visitor = await self.visitor_crud.create_visitor(visitor)
            return created_visitor
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.get("/{visitor_id}", response_model=VisitorOut, status_code=200)
    async def get_visitor_by_id(self, visitor_id: int, current_user: dict = Depends(require_role(["admin", "resident"]))):
        try:
            if current_user is False:
                raise HTTPException(status_code=403, detail="Not authorized to access this visitor")
            visitor_data = await self.visitor_crud.get_visitor_by_id(visitor_id)
            if not visitor_data:
                raise HTTPException(status_code=404, detail="Visitor not found")
            return visitor_data
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.get("/visitorsbycondo/{condo_id}", response_model=List[VisitorOut], status_code=200)
    async def get_visitors_by_condo(self, condo_id: int, current_user: dict = Depends(require_role(["admin", "resident"]))):
        try:
            if current_user is False:
                raise HTTPException(status_code=403, detail="Not authorized to access visitors for this condo")
            visitors_data = await self.visitor_crud.get_visitors_by_condo(condo_id)
            return visitors_data
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.get("/visitorsbyuser/{user_id}", response_model=List[VisitorOut], status_code=200)
    async def get_visitors_by_user(self, user_id: int, current_user: dict = Depends(require_role(["admin", "resident"]))):
        try:
            if current_user is False:
                raise HTTPException(status_code=403, detail="Not authorized to access visitors for this user")
            visitors_data = await self.visitor_crud.get_visitors_by_user(user_id)
            return visitors_data
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.put("/{visitor_id}", response_model=VisitorOut, status_code=200)
    async def update_visitor(self, visitor_id: int, visitor: VisitorUpdate, current_user: dict = Depends(require_role(["admin", "resident"]))):
        try:
            if current_user is False:
                raise HTTPException(status_code=403, detail="Not authorized to update this visitor")
            updated_visitor = await self.visitor_crud.update_visitor(visitor_id, visitor)
            return updated_visitor
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.delete("/{visitor_id}")
    async def delete_visitor(self, visitor_id: int, current_user: dict = Depends(require_role(["admin", "resident"]))):
        try:
            if current_user is False:
                raise HTTPException(status_code=403, detail="Not authorized to delete this visitor")
            await self.visitor_crud.delete_visitor(visitor_id)
            return Response(status_code=204)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
