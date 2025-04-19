from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
import os
from dotenv import load_dotenv
from sqlalchemy.orm import DeclarativeBase

# Load environment variables
load_dotenv()

class Base(DeclarativeBase):
    pass

class AsyncDatabase:
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")
        self.port = int(os.getenv("DB_PORT"))
        if os.getenv("DB_DEV_URL"):
            self.DATABASE_URI = os.getenv("DB_DEV_URL")
        else:
            self.DATABASE_URI = os.getenv("DB_URL")

    async def connect(self):
        try:
            # Create an async engine
            self.engine = create_async_engine(
                self.DATABASE_URI, 
                pool_size=10,         
                max_overflow=20,      
                pool_timeout=30,      
                pool_recycle=3600,    
                echo=True             
            )
            # Create a session maker
            self.SessionLocal = sessionmaker(
                bind=self.engine,
                class_=AsyncSession,  
                expire_on_commit=False
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Could not connect to database: {str(e)}")

    async def get_session(self) -> AsyncSession:
        if not self.SessionLocal:
            await self.connect()
        return self.SessionLocal()

    async def __aenter__(self):
        await self.connect()
        return await self.get_session()

    async def __aexit__(self, exc_type, exc, tb):
        if self.engine:
            await self.engine.dispose()

# Dependency function to get session
async def get_db_session():
    async with AsyncDatabase() as db_session:
        yield db_session
