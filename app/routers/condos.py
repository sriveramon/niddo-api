from fastapi import HTTPException, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from app.schemas.condo import CondoCreate, CondoOut
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

    # @router.get("/amanetiesbycondo/{condo_id}", response_model=CondoOut)
    # async def get_amenities_by_condo(self, condo_id: int):
    #     try:
    #         amenities_data = self.condo_crud.get_all_amenities_for_condo(condo_id)
    #         if not amenities_data:
    #             raise HTTPException(status_code=404, detail="Amenities not found for this condo")
    #         amenities_json = json.dumps([amenitie.model_dump() for amenitie in amenities_data])
    #         return Response(content=amenities_json, status_code=200)
    #     except HTTPException as e:
    #         raise HTTPException(status_code=e.status_code, detail=e.detail)

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
    
    
    # @router.delete("/{amenitie_id}")
    # async def delete_amenitie(self, amenitie_id: int):
    #     try:
    #         self.condo_crud.delete_amenitie(amenitie_id)
    #         return Response(status_code=204)  
    #     except HTTPException as e:
    #         raise HTTPException(status_code=e.status_code, detail=e.detail)