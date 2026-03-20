from fastapi import HTTPException, status

PERMISSIONS = {
    "admin": [
        "providers:create", "providers:read", "providers:update", "providers:delete",
        "patients:create", "patients:read", "patients:update", "patients:delete",
        "visits:create", "visits:read", "visits:update", "visits:delete",
        "treatments:create", "treatments:read", "treatments:update", "treatments:delete",
        "audit:read",
    ],
    "provider": [
        "providers:read", "providers:update_self",
        "patients:create", "patients:read", "patients:update",
        "visits:create", "visits:read", "visits:update",
        "treatments:create", "treatments:read", "treatments:update",
    ],
    "nurse": [
        "providers:read",
        "patients:create", "patients:read",
        "visits:create", "visits:read",
        "treatments:read",
    ],
}


def check_permission(role: str, permission: str) -> bool:
    role_permissions = PERMISSIONS.get(role, [])
    return permission in role_permissions


def require_permission(permission: str):
    from app.auth.dependencies import get_current_user
    from fastapi import Depends

    async def permission_checker(current_user: dict = Depends(get_current_user)):
        if not check_permission(current_user["role"], permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user

    return permission_checker
