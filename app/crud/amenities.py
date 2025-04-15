from app.db import Database
from app.schemas.amenitie import AmenitieCreate
from app.schemas.amenitie import AmenitieOut
from fastapi import HTTPException
import pymysql
from datetime import timedelta

class AmenitiesCRUD:
    def __init__(self):
        self.db = Database()
        
    def timedelta_to_str(self, tdelta: timedelta) -> str:
        total_seconds = int(tdelta.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def create_amenitie(self, amenitie: AmenitieCreate):
        connection = self.db.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO amenities (name, description, start_time, end_time, condo_id) VALUES (%s, %s, %s, %s, %s)",
                    (amenitie.name, amenitie.description, amenitie.start_time, amenitie.end_time, amenitie.condo_id)
                )
                connection.commit()
        except pymysql.MySQLError as e:
            if ('CONSTRAINT \"amenities_ibfk_1\" FOREIGN KEY (\"condo_id\"' in str(e)):
                raise HTTPException(status_code=400, detail="condo_id does not exist")
            raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")
        finally:
            connection.close()

    # def get_amenitie(self, user_id: int) -> AmenitieOut:
    #     connection = self.db.get_connection()
    #     try:
    #         with connection.cursor() as cursor:
    #             cursor.execute("SELECT id, name, email FROM users WHERE id = %s", (user_id,))
    #             result = cursor.fetchone()
    #             if not result:
    #                 raise HTTPException(status_code=404, detail="User not found")
    #             return AmenitieOut(**result)
    #     except pymysql.MySQLError as e:
    #         raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")
    #     finally:
    #         connection.close()
            
    def get_all_amenities_for_condo(self, condo_id) -> list[AmenitieOut]:
        connection = self.db.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT name, description, start_time, end_time FROM amenities where condo_id = %s", (condo_id,))
                result = cursor.fetchall()
                amenities = []
                for amenitie in result:
                    amenitie['start_time'] = self.timedelta_to_str(amenitie['start_time'])
                    amenitie['end_time'] = self.timedelta_to_str(amenitie['end_time'])
                    amenities.append(AmenitieOut(**amenitie))
                return amenities
        except pymysql.MySQLError as e:
            raise HTTPException(status_code=500, detail=f"Error fetching amenities: {str(e)}")
        finally:
            connection.close()
    
    def delete_amenitie(self, amenitie_id: int):
        connection = self.db.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM amenities WHERE id = %s", (amenitie_id,))
                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Amenitie not found")
                connection.commit()
        except pymysql.MySQLError as e:
            raise HTTPException(status_code=500, detail=f"Error deleting amenitie: {str(e)}")
        finally:
            connection.close()
