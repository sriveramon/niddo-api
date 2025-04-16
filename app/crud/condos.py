from app.db import Database
from app.schemas.condo import CondoCreate, CondoOut, CondoUpdate
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
            
    def get_all_condos(self) -> list[CondoOut]:
        connection = self.db.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, name, address FROM condos")
                condos = cursor.fetchall()
                if not condos:
                    raise HTTPException(status_code=404, detail="No condos found")
                return [CondoOut(**condo) for condo in condos]
        except pymysql.MySQLError as e:
            raise HTTPException(status_code=500, detail=f"Error fetching condos: {str(e)}")
        finally:
            connection.close()
            
    def delete_condo(self, condo_id: int):
        connection = self.db.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM condos WHERE id = %s", (condo_id,))
                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Condo not found")
                connection.commit()
        except pymysql.MySQLError as e:
            raise HTTPException(status_code=500, detail=f"Error deleting condo: {str(e)}")
        finally:
            connection.close()
            
    def update_condo(self, condo_id: int, condo: CondoUpdate):
        connection = self.db.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE condos SET name = %s, address = %s WHERE id = %s",
                    (condo.name, condo.address, condo_id)
                )
                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Condo not found")
                connection.commit()
        except pymysql.MySQLError as e:
            raise HTTPException(status_code=500, detail=f"Error updating condo: {str(e)}")
        finally:
            connection.close()