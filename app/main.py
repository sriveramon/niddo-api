from fastapi import FastAPI
from app.routers import users  # We'll create this

app = FastAPI(title="Niddo API")

app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Welcome to Niddo backend!"}
