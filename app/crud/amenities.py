from app.db import Database
from app.schemas.amenity import AmenityCreate, AmenityOut, AmenityUpdate
from fastapi import HTTPException
import pymysql
from datetime import timedelta

class AmenitysCRUD:
    def __init__(self):
        self.db = Database()
        
    def timedelta_to_str(self, tdelta: timedelta) -> str:
        total_seconds = int(tdelta.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def create_amenitie(self, amenity: AmenityCreate):
        connection = self.db.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO amenities (name, description, start_time, end_time, condo_id) VALUES (%s, %s, %s, %s, %s)",
                    (amenity.name, amenity.description, amenity.start_time, amenity.end_time, amenity.condo_id)
                )
                connection.commit()
                amenity_id = cursor.lastrowid
                cursor.execute("SELECT * FROM amenities WHERE id = %s", (amenity_id))
                connection.commit()
                amenity_created = cursor.fetchone()
                amenity_created['start_time'] = self.timedelta_to_str(amenity_created['start_time'])
                amenity_created['end_time'] = self.timedelta_to_str(amenity_created['end_time'])
                return AmenityOut(**amenity_created)
        except pymysql.MySQLError as e:
            if ('CONSTRAINT \"amenities_ibfk_1\" FOREIGN KEY (\"condo_id\"' in str(e)):
                raise HTTPException(status_code=400, detail="condo_id does not exist")
            raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")
        finally:
            connection.close()

    def get_amenitie_by_id(self, amenitie_id: int) -> AmenityOut:
        connection = self.db.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT name, description, start_time, end_time FROM amenities where id = %s", (amenitie_id,))
                amenity = cursor.fetchone()
                if amenity is None:
                    raise HTTPException(status_code=404, detail="Amenity not found")
                amenity['start_time'] = self.timedelta_to_str(amenity['start_time'])
                amenity['end_time'] = self.timedelta_to_str(amenity['end_time'])
                if not amenity:
                    raise HTTPException(status_code=404, detail="Amenity not found")
                return AmenityOut(**amenity)
        except pymysql.MySQLError as e:
            raise HTTPException(status_code=500, detail=f"Error fetching amenity: {str(e)}")
        finally:
            connection.close()
            
    def get_all_amenities_by_condo(self, condo_id) -> list[AmenityOut]:
        connection = self.db.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT name, description, start_time, end_time FROM amenities where condo_id = %s", (condo_id,))
                result = cursor.fetchall()
                if result is None:
                    raise HTTPException(status_code=404, detail="Amenity not found")
                amenities = []
                for amenity in result:
                    amenity['start_time'] = self.timedelta_to_str(amenity['start_time'])
                    amenity['end_time'] = self.timedelta_to_str(amenity['end_time'])
                    amenities.append(AmenityOut(**amenity))
                return amenities
        except pymysql.MySQLError as e:
            raise HTTPException(status_code=500, detail=f"Error fetching amenities: {str(e)}")
        finally:
            connection.close()
            
    def update_amenitie(self, amenitie_id: int, amenity: AmenityUpdate):
        connection = self.db.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE amenities SET name = %s, description = %s, start_time = %s, end_time = %s WHERE id = %s",
                    (amenity.name, amenity.description, amenity.start_time, amenity.end_time, amenitie_id)
                )
                connection.commit()
                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Amenity not found")
                else:
                    cursor.execute("SELECT * FROM amenities WHERE id = %s", (amenitie_id,))
                    amenity_updated = cursor.fetchone()
                    amenity_updated['start_time'] = self.timedelta_to_str(amenity_updated['start_time'])
                    amenity_updated['end_time'] = self.timedelta_to_str(amenity_updated['end_time'])
                    connection.commit()
                    return AmenityOut(**amenity_updated)
                
        except pymysql.MySQLError as e:
            raise HTTPException(status_code=500, detail=f"Error updating amenity: {str(e)}")
        finally:
            connection.close()
    
    def delete_amenitie(self, amenitie_id: int):
        connection = self.db.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM amenities WHERE id = %s", (amenitie_id,))
                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Amenity not found")
                connection.commit()
        except pymysql.MySQLError as e:
            raise HTTPException(status_code=500, detail=f"Error deleting amenity: {str(e)}")
        finally:
            connection.close()
