from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request, status
import bcrypt
from app.database import get_db_connection
from app.schemas.provider import ProviderCreate, ProviderUpdate, ProviderResponse
from app.auth.rbac import require_permission
from app.middleware.audit import log_audit

router = APIRouter(prefix="/providers", tags=["providers"])


@router.post("/", response_model=ProviderResponse, status_code=status.HTTP_201_CREATED)
async def create_provider(
    request: Request,
    provider_data: ProviderCreate,
    current_user: dict = Depends(require_permission("providers:create")),
):
    now = datetime.now(timezone.utc).isoformat()
    password_hash = bcrypt.hashpw(provider_data.password.encode(), bcrypt.gensalt()).decode()

    conn = get_db_connection()
    try:
        cursor = conn.execute(
            """INSERT INTO providers (email, password_hash, first_name, last_name, role, specialty, is_active, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?)""",
            (provider_data.email, password_hash, provider_data.first_name, provider_data.last_name,
             provider_data.role, provider_data.specialty, now, now),
        )
        conn.commit()
        provider_id = cursor.lastrowid

        log_audit(
            user_id=current_user["id"], user_role=current_user["role"],
            action="CREATE", resource_type="provider", resource_id=provider_id,
            details={"email": provider_data.email, "role": provider_data.role},
            ip_address=request.client.host if request.client else None, success=True,
        )

        row = conn.execute("SELECT * FROM providers WHERE id = ?", (provider_id,)).fetchone()
        return _row_to_response(row)
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
        raise
    finally:
        conn.close()


@router.get("/", response_model=list[ProviderResponse])
async def list_providers(
    request: Request,
    current_user: dict = Depends(require_permission("providers:read")),
):
    conn = get_db_connection()
    try:
        rows = conn.execute("SELECT * FROM providers WHERE is_active = 1 ORDER BY id").fetchall()

        log_audit(
            user_id=current_user["id"], user_role=current_user["role"],
            action="READ", resource_type="provider",
            details={"action": "list", "count": len(rows)},
            ip_address=request.client.host if request.client else None, success=True,
        )

        return [_row_to_response(row) for row in rows]
    finally:
        conn.close()


@router.get("/{provider_id}", response_model=ProviderResponse)
async def get_provider(
    provider_id: int,
    request: Request,
    current_user: dict = Depends(require_permission("providers:read")),
):
    conn = get_db_connection()
    try:
        row = conn.execute("SELECT * FROM providers WHERE id = ?", (provider_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")

        log_audit(
            user_id=current_user["id"], user_role=current_user["role"],
            action="READ", resource_type="provider", resource_id=provider_id,
            ip_address=request.client.host if request.client else None, success=True,
        )

        return _row_to_response(row)
    finally:
        conn.close()


@router.put("/{provider_id}", response_model=ProviderResponse)
async def update_provider(
    provider_id: int,
    request: Request,
    provider_data: ProviderUpdate,
    current_user: dict = Depends(require_permission("providers:read")),
):
    # Allow admin full update, or self-update for providers
    is_admin = current_user["role"] == "admin"
    is_self = current_user["id"] == provider_id

    if not is_admin and not is_self:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")

    # Non-admins cannot change role or is_active
    if not is_admin and (provider_data.role is not None or provider_data.is_active is not None):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can change role or status")

    conn = get_db_connection()
    try:
        row = conn.execute("SELECT * FROM providers WHERE id = ?", (provider_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")

        updates = {}
        update_data = provider_data.model_dump(exclude_unset=True)
        if "password" in update_data:
            updates["password_hash"] = bcrypt.hashpw(update_data.pop("password").encode(), bcrypt.gensalt()).decode()
        updates.update(update_data)
        updates["updated_at"] = datetime.now(timezone.utc).isoformat()

        set_clause = ", ".join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [provider_id]
        conn.execute(f"UPDATE providers SET {set_clause} WHERE id = ?", values)
        conn.commit()

        log_audit(
            user_id=current_user["id"], user_role=current_user["role"],
            action="UPDATE", resource_type="provider", resource_id=provider_id,
            details={"updated_fields": list(update_data.keys())},
            ip_address=request.client.host if request.client else None, success=True,
        )

        row = conn.execute("SELECT * FROM providers WHERE id = ?", (provider_id,)).fetchone()
        return _row_to_response(row)
    finally:
        conn.close()


@router.delete("/{provider_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_provider(
    provider_id: int,
    request: Request,
    current_user: dict = Depends(require_permission("providers:delete")),
):
    conn = get_db_connection()
    try:
        row = conn.execute("SELECT * FROM providers WHERE id = ?", (provider_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")

        now = datetime.now(timezone.utc).isoformat()
        conn.execute("UPDATE providers SET is_active = 0, updated_at = ? WHERE id = ?", (now, provider_id))
        conn.commit()

        log_audit(
            user_id=current_user["id"], user_role=current_user["role"],
            action="DELETE", resource_type="provider", resource_id=provider_id,
            ip_address=request.client.host if request.client else None, success=True,
        )
    finally:
        conn.close()


def _row_to_response(row) -> ProviderResponse:
    return ProviderResponse(
        id=row["id"], email=row["email"], first_name=row["first_name"],
        last_name=row["last_name"], role=row["role"], specialty=row["specialty"],
        is_active=bool(row["is_active"]), created_at=row["created_at"], updated_at=row["updated_at"],
    )
