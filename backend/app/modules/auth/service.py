import secrets
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.shared.models import User, Profile, UserPoints
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.core.config import settings
from app.core.logging import logger


async def register_user(db: AsyncSession, email: str, password: str) -> User:
    existing = await db.execute(select(User).where(User.email == email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="E-mail já cadastrado.")

    verification_required = settings.require_email_verification
    token = secrets.token_urlsafe(32) if verification_required else None
    user = User(
        email=email,
        hashed_password=hash_password(password),
        is_verified=not verification_required,
        verification_token=token,
    )
    db.add(user)
    await db.flush()

    # Criar perfil e pontos junto com o usuário
    db.add(Profile(user_id=user.id))
    db.add(UserPoints(user_id=user.id, updated_at=datetime.now(timezone.utc)))

    await db.flush()

    if verification_required:
        await _send_verification_email(email, token)
        logger.info(f"Novo usuário registrado (verificação pendente): id={user.id}")
    else:
        logger.info(f"Novo usuário registrado com acesso direto: id={user.id}")
    return user


async def verify_email(db: AsyncSession, token: str) -> User:
    result = await db.execute(select(User).where(User.verification_token == token))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token de verificação inválido.")
    if user.is_verified:
        # Idempotente: links antigos ou duplo clique não devem gerar erro.
        return user

    user.is_verified = True
    user.verification_token = None
    await db.flush()
    logger.info(f"E-mail verificado: id={user.id}")
    return user


async def login_user(db: AsyncSession, email: str, password: str) -> dict:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="E-mail ou senha incorretos.")
    if not user.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="E-mail não verificado. Verifique sua caixa de entrada.")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Conta desativada.")

    access = create_access_token(str(user.id), user.role.value)
    refresh = create_refresh_token(str(user.id))
    return {"access_token": access, "refresh_token": refresh}


async def refresh_tokens(db: AsyncSession, refresh_token: str) -> dict:
    payload = decode_token(refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido.")

    from app.modules.users.service import get_user_by_id
    user = await get_user_by_id(db, int(payload["sub"]))
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado.")

    access = create_access_token(str(user.id), user.role.value)
    new_refresh = create_refresh_token(str(user.id))
    return {"access_token": access, "refresh_token": new_refresh}


async def request_password_reset(db: AsyncSession, email: str) -> None:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    # Não revelar se o e-mail existe ou não
    if not user:
        return

    token = secrets.token_urlsafe(32)
    user.password_reset_token = token
    user.password_reset_expires = datetime.now(timezone.utc) + timedelta(hours=2)
    await db.flush()
    await _send_password_reset_email(email, token)


async def confirm_password_reset(db: AsyncSession, token: str, new_password: str) -> None:
    result = await db.execute(select(User).where(User.password_reset_token == token))
    user = result.scalar_one_or_none()

    if not user or not user.password_reset_expires:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token inválido ou expirado.")
    if user.password_reset_expires < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token expirado.")

    user.hashed_password = hash_password(new_password)
    user.password_reset_token = None
    user.password_reset_expires = None
    await db.flush()
    logger.info(f"Senha redefinida: id={user.id}")


async def _send_verification_email(email: str, token: str) -> None:
    if not settings.mail_enabled:
        logger.info(f"[MOCK EMAIL] Verificação para {email}: token={token}")
        return
    # TODO: integrar SMTP quando mail_enabled=true


async def _send_password_reset_email(email: str, token: str) -> None:
    if not settings.mail_enabled:
        logger.info(f"[MOCK EMAIL] Reset de senha para {email}: token={token}")
        return
    # TODO: integrar SMTP quando mail_enabled=true
