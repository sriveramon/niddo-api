from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from typing import List
from sqlalchemy.orm import joinedload
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate, ReservationUpdate, ReservationOut


class ReservationCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_reservation(self, reservation: ReservationCreate) -> ReservationOut:
        try:
            new_reservation = Reservation(
                user_id=reservation.user_id,
                amenity_id=reservation.amenity_id,
                date=reservation.date,
                start_time=reservation.start_time,
                end_time=reservation.end_time,
                status=reservation.status
            )
            self.db.add(new_reservation)
            await self.db.commit()
            await self.db.refresh(new_reservation)
            return await self.get_reservation_by_id(new_reservation.id)  # Use the new method to get the reservation with user and amenity details
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating reservation: {str(e)}")

    async def get_reservation_by_id(self, reservation_id: int) -> ReservationOut:
        try:
            query = (
                select(Reservation)
                .options(
                    joinedload(Reservation.user),
                    joinedload(Reservation.amenity)
                )
                .where(Reservation.id == reservation_id)
            )
            result = await self.db.execute(query)
            reservation = result.scalars().first()

            if not reservation:
                raise HTTPException(status_code=404, detail="Reservation not found")

            # Now you can access reservation.user.name and reservation.amenity.name
            return ReservationOut.model_validate({
                "id": reservation.id,
                "date": reservation.date,
                "start_time": reservation.start_time,
                "end_time": reservation.end_time,
                "status": reservation.status,
                "user_name": reservation.user.name,
                "amenity_name": reservation.amenity.name
            })
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching reservation: {str(e)}")

    async def get_reservations_by_user(self, user_id: int) -> List[ReservationOut]:
        try:
            query = (
                select(Reservation)
                .options(
                    joinedload(Reservation.user),
                    joinedload(Reservation.amenity)
                )
                .where(Reservation.user_id == user_id)
            )
            result = await self.db.execute(query)
            reservations = result.scalars().all()

            if not reservations:
                raise HTTPException(status_code=404, detail="Reservations not found")

            return [
                ReservationOut.model_validate({
                    "id": r.id,
                    "date": r.date,
                    "start_time": r.start_time,
                    "end_time": r.end_time,
                    "status": r.status,
                    "user_name": r.user.name,
                    "amenity_name": r.amenity.name
                })
                for r in reservations
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching reservations: {str(e)}")

    async def update_reservation(self, reservation_id: int, data: ReservationUpdate) -> ReservationOut:
        try:
            query = select(Reservation).where(Reservation.id == reservation_id)
            result = await self.db.execute(query)
            reservation = result.scalars().first()

            if not reservation:
                raise HTTPException(status_code=404, detail="Reservation not found")

            reservation.user_id = data.user_id
            reservation.amenity_id = data.amenity_id
            reservation.date = data.date
            reservation.start_time = data.start_time
            reservation.end_time = data.end_time
            reservation.status = data.status

            await self.db.commit()
            await self.db.refresh(reservation)
            return ReservationOut.model_validate(reservation)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating reservation: {str(e)}")

    async def delete_reservation(self, reservation_id: int):
        try:
            query = select(Reservation).where(Reservation.id == reservation_id)
            result = await self.db.execute(query)
            reservation = result.scalars().first()

            if not reservation:
                raise HTTPException(status_code=404, detail="Reservation not found")

            await self.db.delete(reservation)
            await self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting reservation: {str(e)}")
