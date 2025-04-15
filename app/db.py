import pymysql
import os
from dotenv import load_dotenv
from fastapi import HTTPException

# Load environment variables
load_dotenv()

class Database:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")
        self.timeout = 10  # Set a default timeout value

    def get_connection(self):
        try:
            connection = pymysql.connect(
                charset="utf8mb4",
                connect_timeout=self.timeout,
                cursorclass=pymysql.cursors.DictCursor,
                db=self.database,
                host=self.host,
                password=self.password,
                read_timeout=self.timeout,
                port=24905,
                user=self.user,
                write_timeout=self.timeout,
            )
            return connection
        except pymysql.MySQLError as e:
            raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

