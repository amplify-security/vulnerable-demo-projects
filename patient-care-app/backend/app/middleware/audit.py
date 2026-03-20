import json
from datetime import datetime, timezone
from app.database import get_db_connection


def log_audit(
    user_id: int,
    user_role: str,
    action: str,
    resource_type: str,
    resource_id: int = None,
    details: dict = None,
    ip_address: str = None,
    success: bool = True,
):
    conn = get_db_connection()
    try:
        conn.execute(
            """INSERT INTO audit_logs (timestamp, user_id, user_role, action, resource_type, resource_id, details, ip_address, success)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                datetime.now(timezone.utc).isoformat(),
                user_id,
                user_role,
                action,
                resource_type,
                resource_id,
                json.dumps(details) if details else None,
                ip_address,
                success,
            ),
        )
        conn.commit()
    finally:
        conn.close()
