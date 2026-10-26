from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


def error_response(status_code: int, message: str, detail=None):
    body = {"error": {"message": message}}
    if detail:
        body["error"]["detail"] = detail
    return JSONResponse(status_code=status_code, content=body)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [
        {"field": ".".join(str(l) for l in e["loc"]), "message": e["msg"]}
        for e in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": {"message": "Dados inválidos.", "detail": errors}},
    )


async def http_exception_handler(request: Request, exc):
    return error_response(exc.status_code, exc.detail)
