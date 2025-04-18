from fastapi import  Depends, HTTPException
from fastapi_utils.inferring_router import InferringRouter
from app.utils.jwt import create_access_token
from app.db.db import get_db_session
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from app.crud.auth import AuthCRUD

router = InferringRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db_session)):
    login_crud = AuthCRUD(db)
    user = await login_crud.check_login(request)
    if not user or not pwd_context.verify(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"user_id": str(user.id), "user_name": str(user.name), "user_role": user.role, "condo_id": str(user.condo_id)})
    return {"access_token": token}
