from __future__ import annotations

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.domain.errors import DomainError, NotFoundError, ValidationError
from src.interface.http import problem_types

ACCESS_DENIED = "https://api.example.com/problems/access-denied"
CONFLICT = "https://api.example.com/problems/conflict"
INTERNAL_ERROR = "https://api.example.com/problems/internal-error"
UNAUTHORIZED = "https://api.example.com/problems/unauthorized"


def _request_id(request: Request) -> str | None:
    return getattr(request.state, "request_id", None) or request.headers.get(
        "X-Request-ID"
    )


def _correlation_id(request: Request) -> str | None:
    return getattr(request.state, "correlation_id", None) or request.headers.get(
        "X-Correlation-ID"
    )


def _headers(request: Request, extra: dict[str, str] | None = None) -> dict[str, str]:
    headers = dict(extra or {})
    request_id = _request_id(request)
    correlation_id = _correlation_id(request)
    if request_id is not None:
        headers["X-Request-ID"] = request_id
    if correlation_id is not None:
        headers["X-Correlation-ID"] = correlation_id
    return headers


def _problem(
    request: Request,
    *,
    status: int,
    title: str,
    problem_type: str,
    detail: object,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        content={
            "type": problem_type,
            "title": title,
            "status": status,
            "detail": detail,
            "instance": str(request.url.path),
            "request_id": _request_id(request),
            "correlation_id": _correlation_id(request),
        },
        headers=_headers(request, headers),
        media_type="application/problem+json",
    )


async def domain_error_handler(request: Request, exc: Exception) -> JSONResponse:
    mapping: dict[type[Exception], tuple[int, str, str]] = {
        ValidationError: (422, "Ошибка валидации", problem_types.VALIDATION),
        NotFoundError: (404, "Не найдено", problem_types.NOT_FOUND),
    }
    status, title, problem_type = mapping.get(
        type(exc),
        (500, "Внутренняя ошибка", "about:blank"),
    )
    return _problem(
        request,
        status=status,
        title=title,
        problem_type=problem_type,
        detail=str(exc),
    )


async def unexpected_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return _problem(
        request,
        status=500,
        title="Внутренняя ошибка",
        problem_type=INTERNAL_ERROR,
        detail="Unhandled server error.",
    )


async def validation_error_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return _problem(
        request,
        status=422,
        title="Ошибка валидации",
        problem_type=problem_types.VALIDATION,
        detail=str(exc),
    )


async def http_error_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    mapping = {
        401: ("Не авторизован", UNAUTHORIZED),
        403: ("Доступ запрещен", ACCESS_DENIED),
        404: ("Не найдено", problem_types.NOT_FOUND),
        409: ("Конфликт", CONFLICT),
        422: ("Ошибка валидации", problem_types.VALIDATION),
    }
    title, problem_type = mapping.get(exc.status_code, (str(exc.detail), "about:blank"))
    return _problem(
        request,
        status=exc.status_code,
        title=title,
        problem_type=problem_type,
        detail=exc.detail,
        headers=exc.headers,
    )


def register_exception_handlers(app) -> None:
    app.add_exception_handler(DomainError, domain_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(StarletteHTTPException, http_error_handler)
    app.add_exception_handler(Exception, unexpected_error_handler)
