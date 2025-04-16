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
        self.DATABASE_URI = f"mysql+aiomysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    async def connect(self):
        try:
            # Create an async engine
            self.engine = create_async_engine(
                self.DATABASE_URI, 
                pool_size=10,         # Maximum number of connections in the pool
                max_overflow=20,      # Allow connections beyond pool_size
                pool_timeout=30,      # Max time to wait for a connection
                pool_recycle=3600,    # Maximum time for a connection to be reused
                echo=True             # Print SQL queries (for debugging)
            )
            # Create a session maker
            self.SessionLocal = sessionmaker(
                bind=self.engine,
                class_=AsyncSession,  # Use AsyncSession for async operations
                expire_on_commit=False
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Could not connect to database: {str(e)}")

    async def get_session(self) -> AsyncSession:
        if not self.SessionLocal:
            await self.connect()
        # Return a new session from the connection pool
        return self.SessionLocal()

    async def __aenter__(self):
        await self.connect()
        return await self.get_session()

    async def __aexit__(self, exc_type, exc, tb):
        if self.engine:
            # Dispose of the engine to close connections in the pool
            await self.engine.dispose()

# Dependency function to get session
async def get_db_session():
    async with AsyncDatabase() as db_session:
        yield db_session
