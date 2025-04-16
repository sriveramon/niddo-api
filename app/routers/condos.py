from fastapi import HTTPException, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from app.schemas.condo import CondoCreate, CondoOut, CondoUpdate
from app.crud.condos import CondosCRUD
import json

router = InferringRouter(prefix="/condos", tags=["condos"])
@cbv(router)
class CondosRoutes:
    def __init__(self):
        self.condo_crud = CondosCRUD()

    @router.post("/", response_model=CondoOut, )
    async def create_condo(self, condo: CondoCreate):
        try:
            self.condo_crud.create_condo(condo)

            # Now create a dictionary or model to serialize
            condo_json = json.dumps(condo.model_dump())
            return Response(content=condo_json, status_code=201)  # Created

        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.get("/{condo_id}", response_model=CondoOut)
    async def get_amenitie_by_id(self, condo_id: int):
        try:
            condo_data = self.condo_crud.get_condo_by_id(condo_id)
            if not condo_data:
                raise HTTPException(status_code=404, detail="Condo not found")
            amenitie_json = json.dumps(condo_data.model_dump())
            return Response(content=amenitie_json, status_code=200)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        
    @router.get("/", response_model=list[CondoOut])
    async def get_all_condos(self):
        try:
            condos_data = self.condo_crud.get_all_condos()
            if not condos_data:
                raise HTTPException(status_code=404, detail="No condos found")
            condos_json = json.dumps([condo.model_dump() for condo in condos_data])
            return Response(content=condos_json, status_code=200)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        
    @router.put("/{condo_id}", response_model=CondoOut)
    async def update_condo(self, condo_id: int, condo: CondoUpdate):
        try:
            self.condo_crud.update_condo(condo_id, condo)
            updated_condo_json = json.dumps(condo.model_dump())
            return Response(content=updated_condo_json, status_code=200)  
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    @router.delete("/{condo_id}")
    async def delete_condo(self, condo_id: int):
        try:
            self.condo_crud.delete_condo(condo_id)
            return Response(status_code=204)  
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
    