from __future__ import annotations

from dataclasses import dataclass

from fastapi import Depends, Header, HTTPException, status

from src.infrastructure.config.settings import Settings
from src.interface.http.wiring import get_settings


def require_service_token(
    settings: Settings = Depends(get_settings),
    x_service_token: str | None = Header(default=None, alias="X-Service-Token"),
) -> None:
    if not x_service_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Требуется X-Service-Token.",
        )
    if x_service_token != settings.service_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректный X-Service-Token.",
        )


@dataclass(frozen=True)
class InternalActorContext:
    user_id: str
    roles: tuple[str, ...]


def _parse_actor_roles(raw_roles: str | None) -> tuple[str, ...]:
    if not raw_roles:
        return ()

    return tuple(role.strip() for role in raw_roles.split(",") if role.strip())


def require_admin_actor(
    x_actor_user_id: str | None = Header(default=None, alias="X-Actor-User-Id"),
    x_actor_roles: str | None = Header(default=None, alias="X-Actor-Roles"),
) -> InternalActorContext:
    roles = _parse_actor_roles(x_actor_roles)

    if not x_actor_user_id or not roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Требуется actor context для изменения offer.",
        )

    if "admin" not in roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Изменение offer доступно только admin actor.",
        )

    return InternalActorContext(user_id=x_actor_user_id, roles=roles)
