from fastapi import HTTPException, Depends, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.reservation import ReservationCreate, ReservationOut, ReservationUpdate
from app.crud.reservartions import ReservationCRUD
from app.db.db import get_db_session
from app.dependencies.auth import require_role# Import get_current_user dependency

router = InferringRouter(prefix="/reservations", tags=["reservations"])

@cbv(router)
class ReservationsRoutes:
    def __init__(self, db: AsyncSession = Depends(get_db_session)):
        self.reservation_crud = ReservationCRUD(db)

    @router.post("/", response_model=ReservationOut, status_code=201)
    async def create_reservation(self, reservation: ReservationCreate, current_user: dict = Depends(require_role(["admin", "resident"]))):
        try:
            if current_user is not True:
                raise HTTPException(status_code=403, detail="Not authorized to create this reservation")
            created_reservation = await self.reservation_crud.create_reservation(reservation)
            return created_reservation
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.get("/{reservation_id}", response_model=ReservationOut, status_code=200)
    async def get_reservation_by_id(self, reservation_id: int, current_user: dict = Depends(require_role(["admin", "resident"]))):
        try:
            if current_user is not True:
                raise HTTPException(status_code=403, detail="Not authorized to access this reservation")
            reservation_data = await self.reservation_crud.get_reservation_by_id(reservation_id)
            if not reservation_data:
                raise HTTPException(status_code=404, detail="Reservation not found")
            return reservation_data
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.get("/reservationsbyuser/{user_id}", response_model=List[ReservationOut], status_code=200)
    async def get_reservations_by_user(self, user_id: int, current_user: dict = Depends(require_role(["admin", "resident"]))):
        try:
            if current_user is not True:
                raise HTTPException(status_code=403, detail="Not authorized to access reservations for this user")
            reservations_data = await self.reservation_crud.get_reservations_by_user(user_id)
            if not reservations_data:
                raise HTTPException(status_code=404, detail="No reservations found for this user")
            return reservations_data
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.put("/{reservation_id}", response_model=ReservationOut, status_code=200)
    async def update_reservation(self, reservation_id: int, reservation: ReservationUpdate, current_user: dict = Depends(require_role(["admin", "resident"]))):
        try:
            if current_user is not True:
                raise HTTPException(status_code=403, detail="Not authorized to update this reservation")
            updated_reservation = await self.reservation_crud.update_reservation(reservation_id, reservation)
            return updated_reservation
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    @router.delete("/{reservation_id}")
    async def delete_reservation(self, reservation_id: int, current_user: dict = Depends(require_role(["admin", "resident"]))):
        try:
            if current_user is not True:
                raise HTTPException(status_code=403, detail="Not authorized to delete this reservation")
            await self.reservation_crud.delete_reservation(reservation_id)
            return Response(status_code=204)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
