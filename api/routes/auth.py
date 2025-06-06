from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Dict, Any

from ..models.schemas import Token, User, SessionResponse
from ..services.auth_service import auth_service, fake_users_db
from ..utils.config import config

router = APIRouter(prefix="", tags=["authentication"])

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Endpoint para autenticación y obtención de token"""
    user = auth_service.authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/api/v1/auth/session", response_model=SessionResponse)
async def get_session(current_user: User = Depends(auth_service.get_current_active_user)):
    """Obtiene información de la sesión actual"""
    return SessionResponse(
        uid=1,
        username=current_user.username,
        name=current_user.full_name or current_user.username,
        session_id=auth_service.generate_session_id(),
        db=config.ODOO_DB
    )
