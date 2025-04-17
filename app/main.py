from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.db import AsyncDatabase  # Import the AsyncDatabase class
from app.db.db import AsyncDatabase as db  # Your AsyncDatabase singleton
from app.routers.users import router as user_router
from app.routers.amenities import router as amenity_router
from app.routers.condos import router as condo_router
from app.routers.reservations import router as reservation_router
from app.routers.auth import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = AsyncDatabase()  # Instantiate the AsyncDatabase class
    await db.connect()    # Now call the connect method on the instance
    print("✅ Database connected")

    yield  # <-- The app runs during this yield

    await db.close()      # Call the close method on the instance
    print("🛑 Database disconnected")

app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(user_router)
app.include_router(amenity_router)
app.include_router(condo_router)
app.include_router(reservation_router)
app.include_router(auth_router)