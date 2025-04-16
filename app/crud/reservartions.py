from app.db import Database
from app.schemas.reservation import ReservationCreate, ReservationOut, ReservationUpdate
from fastapi import HTTPException
import pymysql
from datetime import timedelta

class ReservationsCRUD:
    def __init__(self):
        self.db = Database()
        
    def timedelta_to_str(self, tdelta: timedelta) -> str:
        total_seconds = int(tdelta.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def create_reservation(self, reservation: ReservationCreate):
        connection = self.db.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO reservations (user_id, amenity_id, date, start_time, end_time, status) VALUES (%s, %s, %s, %s, %s, %s)",
                    (reservation.user_id, reservation.amenity_id, reservation.date, reservation.start_time, reservation.end_time, reservation.status)
                )
                new_reservation_id = cursor.lastrowid
                connection.commit()
                return new_reservation_id
        except pymysql.MySQLError as e:
            if ('CONSTRAINT \"amenities_ibfk_1\" FOREIGN KEY (\"condo_id\"' in str(e)):
                raise HTTPException(status_code=400, detail="condo_id does not exist")
            raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")
        finally:
            connection.close()
            
    def get_reservation_by_id(self, reservation_id: int) -> ReservationOut:
        connection = self.db.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT 
                        reservation.id,
                        reservation.date,
                        reservation.start_time,
                        reservation.end_time,
                        reservation.status,
                        user.name AS user_name,
                        amenity.name AS amenity_name
                    FROM reservations reservation
                    JOIN users user ON reservation.user_id = user.id
                    JOIN amenities amenity ON reservation.amenity_id = amenity.id
                    WHERE reservation.id = %s""", 
                    reservation_id)
                reservation = cursor.fetchone()
                if reservation is None:
                    raise HTTPException(status_code=404, detail="Reservation not found")
                reservation['start_time'] = self.timedelta_to_str(reservation['start_time'])
                reservation['end_time'] = self.timedelta_to_str(reservation['end_time'])
                reservation['date'] = reservation['date'].strftime('%Y-%m-%d')
                if not reservation:
                    raise HTTPException(status_code=404, detail="Reservation not found")
                return ReservationOut(**reservation)
        except pymysql.MySQLError as e:
            raise HTTPException(status_code=500, detail=f"Error fetching reservation: {str(e)}")
        finally:
            connection.close()
            
    def get_reservations_by_user(self, user_id: int) -> list[ReservationOut]:
        connection = self.db.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT 
                        reservation.id,
                        reservation.date,
                        reservation.start_time,
                        reservation.end_time,
                        reservation.status,
                        user.name AS user_name,
                        amenity.name AS amenity_name
                    FROM reservations reservation
                    JOIN users user ON reservation.user_id = user.id
                    JOIN amenities amenity ON reservation.amenity_id = amenity.id
                    WHERE reservation.user_id = %s""", 
                    (user_id,))
                result = cursor.fetchall()
                if result is None:
                    raise HTTPException(status_code=404, detail="Reservation not found")
                reservations = []
                for reservation in result:
                    reservation['start_time'] = self.timedelta_to_str(reservation['start_time'])
                    reservation['end_time'] = self.timedelta_to_str(reservation['end_time'])
                    reservation['date'] = reservation['date'].strftime('%Y-%m-%d')
                    reservations.append(ReservationOut(**reservation))
                return reservations
        except pymysql.MySQLError as e:
            raise HTTPException(status_code=500, detail=f"Error fetching reservations: {str(e)}")
        finally:
            connection.close()

    # def get_amenitie_by_id(self, amenitie_id: int) -> ReservationOut:
    #     connection = self.db.get_connection()
    #     try:
    #         with connection.cursor() as cursor:
    #             cursor.execute("SELECT name, description, start_time, end_time FROM amenities where id = %s", (amenitie_id,))
    #             amenity = cursor.fetchone()
    #             if amenity is None:
    #                 raise HTTPException(status_code=404, detail="Reservation not found")
    #             amenity['start_time'] = self.timedelta_to_str(amenity['start_time'])
    #             amenity['end_time'] = self.timedelta_to_str(amenity['end_time'])
    #             if not amenity:
    #                 raise HTTPException(status_code=404, detail="Reservation not found")
    #             return ReservationOut(**amenity)
    #     except pymysql.MySQLError as e:
    #         raise HTTPException(status_code=500, detail=f"Error fetching amenity: {str(e)}")
    #     finally:
    #         connection.close()
            
    # def get_all_amenities_for_condo(self, condo_id) -> list[ReservationOut]:
    #     connection = self.db.get_connection()
    #     try:
    #         with connection.cursor() as cursor:
    #             cursor.execute("SELECT name, description, start_time, end_time FROM amenities where condo_id = %s", (condo_id,))
    #             result = cursor.fetchall()
    #             if result is None:
    #                 raise HTTPException(status_code=404, detail="Reservation not found")
    #             amenities = []
    #             for amenity in result:
    #                 amenity['start_time'] = self.timedelta_to_str(amenity['start_time'])
    #                 amenity['end_time'] = self.timedelta_to_str(amenity['end_time'])
    #                 amenities.append(ReservationOut(**amenity))
    #             return amenities
    #     except pymysql.MySQLError as e:
    #         raise HTTPException(status_code=500, detail=f"Error fetching amenities: {str(e)}")
    #     finally:
    #         connection.close()
            
    # def update_amenitie(self, amenitie_id: int, amenity: ReservationUpdate):
    #     connection = self.db.get_connection()
    #     try:
    #         with connection.cursor() as cursor:
    #             cursor.execute(
    #                 "UPDATE amenities SET name = %s, description = %s, start_time = %s, end_time = %s WHERE id = %s",
    #                 (amenity.name, amenity.description, amenity.start_time, amenity.end_time, amenitie_id)
    #             )
    #             if cursor.rowcount == 0:
    #                 raise HTTPException(status_code=404, detail="Reservation not found")
    #             connection.commit()
    #     except pymysql.MySQLError as e:
    #         raise HTTPException(status_code=500, detail=f"Error updating amenity: {str(e)}")
    #     finally:
    #         connection.close()
    
    # def delete_amenitie(self, amenitie_id: int):
    #     connection = self.db.get_connection()
    #     try:
    #         with connection.cursor() as cursor:
    #             cursor.execute("DELETE FROM amenities WHERE id = %s", (amenitie_id,))
    #             if cursor.rowcount == 0:
    #                 raise HTTPException(status_code=404, detail="Reservation not found")
    #             connection.commit()
    #     except pymysql.MySQLError as e:
    #         raise HTTPException(status_code=500, detail=f"Error deleting amenity: {str(e)}")
    #     finally:
    #         connection.close()
