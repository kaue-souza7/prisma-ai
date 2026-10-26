from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.auth import service
from app.modules.auth.schemas import (
    RegisterRequest, LoginRequest, TokenResponse,
    RefreshRequest, PasswordResetRequest, PasswordResetConfirm, MessageResponse
)

router = APIRouter()


@router.post("/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest, db: AsyncSession = Depends(get_db)):
    await service.register_user(db, body.email, body.password)
    return {"message": "Cadastro realizado. Verifique seu e-mail para ativar a conta."}


@router.get("/verify-email", response_model=MessageResponse)
async def verify_email(token: str, db: AsyncSession = Depends(get_db)):
    await service.verify_email(db, token)
    return {"message": "E-mail verificado com sucesso. Você já pode fazer login."}


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    tokens = await service.login_user(db, body.email, body.password)
    return tokens


@router.post("/refresh", response_model=TokenResponse)
async def refresh(body: RefreshRequest, db: AsyncSession = Depends(get_db)):
    tokens = await service.refresh_tokens(db, body.refresh_token)
    return tokens


@router.post("/password-reset/request", response_model=MessageResponse)
async def request_reset(body: PasswordResetRequest, db: AsyncSession = Depends(get_db)):
    await service.request_password_reset(db, body.email)
    return {"message": "Se o e-mail estiver cadastrado, você receberá as instruções em breve."}


@router.post("/password-reset/confirm", response_model=MessageResponse)
async def confirm_reset(body: PasswordResetConfirm, db: AsyncSession = Depends(get_db)):
    await service.confirm_password_reset(db, body.token, body.new_password)
    return {"message": "Senha redefinida com sucesso."}
