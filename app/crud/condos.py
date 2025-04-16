from app.db import Database
from app.schemas.condo import CondoCreate
from app.schemas.condo import CondoOut
from fastapi import HTTPException
import pymysql

class CondosCRUD:
    def __init__(self):
        self.db = Database()

    def create_condo(self, condo: CondoCreate):
        connection = self.db.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO condos (name, address) VALUES (%s, %s)",
                    (condo.name, condo.address)
                )
                connection.commit()
        except pymysql.MySQLError as e:
            raise HTTPException(status_code=500, detail=f"Error creating condo: {str(e)}")
        finally:
            connection.close()

    def get_condo_by_id(self, condo_id: int) -> CondoOut:
        connection = self.db.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT name, address FROM condos where id = %s", (condo_id,))
                condo = cursor.fetchone()
                if condo is None:
                    raise HTTPException(status_code=404, detail="Condo not found")
                return CondoOut(**condo)
        except pymysql.MySQLError as e:
            raise HTTPException(status_code=500, detail=f"Error fetching condo: {str(e)}")
        finally:
            connection.close()
            
    # def get_all_amenities_for_condo(self, condo_id) -> list[CondoOut]:
    #     connection = self.db.get_connection()
    #     try:
    #         with connection.cursor() as cursor:
    #             cursor.execute("SELECT name, description, start_time, end_time FROM amenities where condo_id = %s", (condo_id,))
    #             result = cursor.fetchall()
    #             if result is None:
    #                 raise HTTPException(status_code=404, detail="Amenitie not found")
    #             amenities = []
    #             for amenitie in result:
    #                 amenitie['start_time'] = self.timedelta_to_str(amenitie['start_time'])
    #                 amenitie['end_time'] = self.timedelta_to_str(amenitie['end_time'])
    #                 amenities.append(CondoOut(**amenitie))
    #             return amenities
    #     except pymysql.MySQLError as e:
    #         raise HTTPException(status_code=500, detail=f"Error fetching amenities: {str(e)}")
    #     finally:
    #         connection.close()
    
    # def delete_amenitie(self, amenitie_id: int):
    #     connection = self.db.get_connection()
    #     try:
    #         with connection.cursor() as cursor:
    #             cursor.execute("DELETE FROM amenities WHERE id = %s", (amenitie_id,))
    #             if cursor.rowcount == 0:
    #                 raise HTTPException(status_code=404, detail="Amenitie not found")
    #             connection.commit()
    #     except pymysql.MySQLError as e:
    #         raise HTTPException(status_code=500, detail=f"Error deleting amenitie: {str(e)}")
    #     finally:
    #         connection.close()
