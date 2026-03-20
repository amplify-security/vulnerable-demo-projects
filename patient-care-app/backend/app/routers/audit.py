import json
from fastapi import APIRouter, Depends, Request
from app.database import get_db_connection
from app.auth.rbac import require_permission
from app.middleware.audit import log_audit

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("/logs")
async def get_audit_logs(
    request: Request,
    resource_type: str = None,
    user_id: int = None,
    action: str = None,
    start_date: str = None,
    end_date: str = None,
    limit: int = 100,
    offset: int = 0,
    current_user: dict = Depends(require_permission("audit:read")),
):
    conn = get_db_connection()
    try:
        query = "SELECT * FROM audit_logs WHERE 1=1"
        params = []

        if resource_type:
            query += " AND resource_type = ?"
            params.append(resource_type)
        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)
        if action:
            query += " AND action = ?"
            params.append(action)
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date)
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date)

        query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
        params.extend([min(limit, 1000), offset])

        rows = conn.execute(query, params).fetchall()

        log_audit(
            user_id=current_user["id"], user_role=current_user["role"],
            action="READ", resource_type="audit",
            details={"action": "list", "count": len(rows)},
            ip_address=request.client.host if request.client else None, success=True,
        )

        results = []
        for row in rows:
            results.append({
                "id": row["id"],
                "timestamp": row["timestamp"],
                "user_id": row["user_id"],
                "user_role": row["user_role"],
                "action": row["action"],
                "resource_type": row["resource_type"],
                "resource_id": row["resource_id"],
                "details": json.loads(row["details"]) if row["details"] else None,
                "ip_address": row["ip_address"],
                "success": bool(row["success"]),
            })

        return {"logs": results, "count": len(results), "offset": offset}
    finally:
        conn.close()
