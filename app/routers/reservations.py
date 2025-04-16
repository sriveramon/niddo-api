from fastapi import HTTPException, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from app.schemas.reservation import ReservationCreate, ReservationOut, ReservationUpdate
from app.crud.reservartions import ReservationsCRUD
import json

router = InferringRouter(prefix="/reservations", tags=["reservations"])
@cbv(router)
class AmenitysRoutes:
    def __init__(self):
        self.reservation_crud = ReservationsCRUD()

    @router.post("/", response_model=ReservationOut, )
    async def create_reservation(self, reservation: ReservationCreate):
        try:
            new_reservation_id = self.reservation_crud.create_reservation(reservation)
            new_reservation_data = self.reservation_crud.get_reservation_by_id(new_reservation_id)
            if not new_reservation_data:
                raise HTTPException(status_code=404, detail="Reservation not found")

            # Now create a dictionary or model to serialize
            reservation_json = json.dumps(new_reservation_data.model_dump())
            return Response(content=reservation_json, status_code=201)  # Created

        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        
    @router.get("/{reservation_id}", response_model=ReservationOut)
    async def get_reservation_by_id(self, reservation_id: int):
        try:
            reservation_data = self.reservation_crud.get_reservation_by_id(reservation_id)
            if not reservation_data:
                raise HTTPException(status_code=404, detail="Reservation not found")
            reservation_json = json.dumps(reservation_data.model_dump())
            return Response(content=reservation_json, status_code=200)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        
    @router.get("/reservationsbyuser/{user_id}", response_model=ReservationOut)
    async def get_reservations_by_user(self, user_id: int):
        try:
            reservations_data = self.reservation_crud.get_reservations_by_user(user_id)
            if not reservations_data:
                raise HTTPException(status_code=404, detail="Reservations not found for this user")
            reservations_json = json.dumps([reservation.model_dump() for reservation in reservations_data])
            return Response(content=reservations_json, status_code=200)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        
    @router.put("/{reservation_id}", response_model=ReservationOut)
    async def update_reservation(self, reservation_id: int, reservation: ReservationUpdate):
        try:
            self.reservation_crud.update_reservation(reservation_id, reservation)
            updated_reservation_data = self.reservation_crud.get_reservation_by_id(reservation_id)
            if not updated_reservation_data:
                raise HTTPException(status_code=404, detail="Reservation not found")
            
            # Now create a dictionary or model to serialize
            updated_reservation_json = json.dumps(updated_reservation_data.model_dump())
            return Response(content=updated_reservation_json, status_code=200)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        
    @router.delete("/{reservation_id}")
    async def delete_reservation(self, reservation_id: int):
        try:
            self.reservation_crud.delete_reservation(reservation_id)
            return Response(status_code=204)  
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
