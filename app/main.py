from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ⬅️ Add this line
from contextlib import asynccontextmanager
from app.db.db import AsyncDatabase  # Import the AsyncDatabase class
from app.db.db import AsyncDatabase as db  # Your AsyncDatabase singleton
from app.routers.users import router as user_router
from app.routers.amenities import router as amenity_router
from app.routers.condos import router as condo_router
from app.routers.reservations import router as reservation_router
from app.routers.auth import router as auth_router
from app.routers.blocks import router as block_router
from app.routers.visitors import router as visitor_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = AsyncDatabase()
    await db.connect()
    print("✅ Database connected")

    yield

    await db.close()
    print("🛑 Database disconnected")

app = FastAPI(lifespan=lifespan)

# ✅ CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend origin for security in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_router)
app.include_router(amenity_router)
app.include_router(condo_router)
app.include_router(reservation_router)
app.include_router(auth_router)
app.include_router(block_router)
app.include_router(visitor_router)
