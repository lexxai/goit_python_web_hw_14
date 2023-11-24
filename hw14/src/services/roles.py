import logging
from typing import Any, List

from fastapi import Depends, HTTPException, status, Request

from src.conf.config import settings
from src.database.models import Role, User
from src.routes import auth

logger = logging.getLogger(f"{settings.app_name}.{__name__}")

class RoleAccess:

    def __init__(self, allowed_roles: List[Role]) -> None:
        self.allowed_roles = allowed_roles

    async def __call__(self, request: Request, current_user: User = Depends(auth.get_current_user)) -> Any:
        logger.debug(f"{request.method=}, {request.url=}")
        if current_user:
            logger.debug(f"User role: {current_user.role}")
            logger.debug(f"Allower roles: {self.allowed_roles}")
        if current_user.role not in self.allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation frobidden")