from app.db import Database
from app.schemas.user import UserCreate, UserOut
from fastapi import HTTPException
import pymysql

class UserCRUD:
    def __init__(self):
        self.db = Database()

    def create_user(self, user: UserCreate):
        connection = self.db.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (name, email, password_hash, condo_id, unit) VALUES (%s, %s, %s, %s, %s)",
                    (user.name, user.email, user.password, user.condo_id, user.unit)
                )
                connection.commit()
        except pymysql.MySQLError as e:
            if ('CONSTRAINT \"fk_users_condo\" FOREIGN KEY (\"condo_id\"' in str(e)):
                raise HTTPException(status_code=400, detail="condo_id does not exist")
            raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")
        finally:
            connection.close()

    def get_user(self, user_id: int) -> UserOut:
        connection = self.db.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, name, email FROM users WHERE id = %s", (user_id,))
                result = cursor.fetchone()
                if not result:
                    raise HTTPException(status_code=404, detail="User not found")
                return UserOut(**result)
        except pymysql.MySQLError as e:
            raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")
        finally:
            connection.close()
            
    def get_all_users(self) -> list[UserOut]:
        connection = self.db.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, name, email FROM users")
                result = cursor.fetchall()
                return [UserOut(**user) for user in result]
        except pymysql.MySQLError as e:
            raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")
        finally:
            connection.close()
            
    def get_users_by_condo(self, condo_id: int) -> list[UserOut]:
        connection = self.db.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, name, email FROM users WHERE condo_id = %s", (condo_id,))
                result = cursor.fetchall()
                return [UserOut(**user) for user in result]
        except pymysql.MySQLError as e:
            raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")
        finally:
            connection.close()
    
    def delete_user(self, user_id: int):
        connection = self.db.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail="User not found")
                connection.commit()
        except pymysql.MySQLError as e:
            raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")
        finally:
            connection.close()
