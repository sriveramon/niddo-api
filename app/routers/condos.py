from fastapi import HTTPException, Response, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from app.schemas.condo import CondoCreate, CondoOut, CondoUpdate
from app.crud.condos import CondosCRUD
from app.db.db import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

router = InferringRouter(prefix="/condos", tags=["condos"])

@cbv(router)
class CondosRoutes:
    def __init__(self, db: AsyncSession = Depends(get_db_session)):
        self.condo_crud = CondosCRUD(db)

    @router.post("/", response_model=CondoOut, status_code=201)
    async def create_condo(self, condo: CondoCreate):
        try:
            created_condo = await self.condo_crud.create_condo(condo)
            return created_condo  # FastAPI automatically serializes the response with Pydantic model
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.get("/{condo_id}", response_model=CondoOut, status_code=200)
    async def get_condo_by_id(self, condo_id: int):
        try:
            condo_data = await self.condo_crud.get_condo_by_id(condo_id)
            if not condo_data:
                raise HTTPException(status_code=404, detail="Condo not found")
            return condo_data
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.get("/", response_model=list[CondoOut], status_code=200)
    async def get_all_condos(self):
        try:
            condos_data = await self.condo_crud.get_all_condos()
            if not condos_data:
                raise HTTPException(status_code=404, detail="No condos found")
            return condos_data
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.put("/{condo_id}", response_model=CondoOut, status_code=200)
    async def update_condo(self, condo_id: int, condo: CondoUpdate):
        try:
            updated_condo = await self.condo_crud.update_condo(condo_id, condo)
            return updated_condo
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.delete("/{condo_id}", status_code=204)
    async def delete_condo(self, condo_id: int):
        try:
            await self.condo_crud.delete_condo(condo_id)
            return Response(status_code=204)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
