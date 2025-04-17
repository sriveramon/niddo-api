from fastapi import HTTPException, Response, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from app.schemas.condo import CondoCreate, CondoOut, CondoUpdate
from app.crud.condos import CondosCRUD
from app.db.db import get_db_session
from app.dependencies.auth import require_role# Import get_current_user dependency
from sqlalchemy.ext.asyncio import AsyncSession

router = InferringRouter(prefix="/condos", tags=["condos"])

@cbv(router)
class CondosRoutes:
    def __init__(self, db: AsyncSession = Depends(get_db_session)):
        self.condo_crud = CondosCRUD(db)

    @router.post("/", response_model=CondoOut, status_code=201)
    async def create_condo(self, condo: CondoCreate, current_user: dict = Depends(require_role(["admin", "resident"]))):
        try:
            if current_user is not True:
                raise HTTPException(status_code=403, detail="Not authorized to create this condo")
            created_condo = await self.condo_crud.create_condo(condo)
            return created_condo
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.get("/{condo_id}", response_model=CondoOut, status_code=200)
    async def get_condo_by_id(self, condo_id: int, current_user: dict = Depends(require_role(["admin", "resident"]))):
        try:
            if current_user is not True:
                raise HTTPException(status_code=403, detail="Not authorized to access this condo")
            condo_data = await self.condo_crud.get_condo_by_id(condo_id)
            if not condo_data:
                raise HTTPException(status_code=404, detail="Condo not found")
            return condo_data
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.get("/", response_model=list[CondoOut], status_code=200)
    async def get_all_condos(self, current_user: dict = Depends(require_role(["admin", "resident"]))):
        try:
            if current_user is not True:
                raise HTTPException(status_code=403, detail="Not authorized to access all condos")
            condos_data = await self.condo_crud.get_all_condos()
            if not condos_data:
                raise HTTPException(status_code=404, detail="No condos found")
            return condos_data
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.put("/{condo_id}", response_model=CondoOut, status_code=200)
    async def update_condo(self, condo_id: int, condo: CondoUpdate, current_user: dict = Depends(require_role(["admin", "resident"]))):
        try:
            if current_user is not True:
                raise HTTPException(status_code=403, detail="Not authorized to update this condo")
            updated_condo = await self.condo_crud.update_condo(condo_id, condo)
            return updated_condo
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.delete("/{condo_id}", status_code=204)
    async def delete_condo(self, condo_id: int, current_user: dict = Depends(require_role(["admin", "resident"]))):
        try:
            if current_user is not True:
                raise HTTPException(status_code=403, detail="Not authorized to delete this condo")
            await self.condo_crud.delete_condo(condo_id)
            return Response(status_code=204)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
