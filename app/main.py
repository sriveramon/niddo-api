from fastapi import FastAPI
from app.routers.users import router as user_router
from app.routers.amenities import router as amenity_router

app = FastAPI()

# Include routers
app.include_router(user_router)
app.include_router(amenity_router)