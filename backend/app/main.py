from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.exceptions import validation_exception_handler, http_exception_handler

from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.modules.journey.router import router as journey_router
from app.modules.progress.router import router as progress_router
from app.modules.content.router import router as content_router
from app.modules.conversations.router import router as conversations_router
from app.modules.studio.router import router as studio_router

setup_logging()

app = FastAPI(
    title="Prisma.AI API",
    description="Plataforma de educação financeira personalizada para jovens adultos.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Handlers de erro
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)

# Routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(journey_router, prefix="/api/v1/journey", tags=["journey"])
app.include_router(progress_router, prefix="/api/v1/progress", tags=["progress"])
app.include_router(content_router, prefix="/api/v1/content", tags=["content"])
app.include_router(conversations_router, prefix="/api/v1/conversations", tags=["conversations"])
app.include_router(studio_router, prefix="/api/v1/studio", tags=["studio"])


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok", "version": "0.1.0"}
