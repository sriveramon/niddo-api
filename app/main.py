from fastapi import FastAPI
from app.routers.users import router as user_router

app = FastAPI()

# Include routers
app.include_router(user_router)
