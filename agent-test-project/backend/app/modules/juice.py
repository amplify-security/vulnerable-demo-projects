import logging

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse

from app.database import get_db_connection
from app.modules.domain_models import Juice

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/juices", response_model=list[Juice])
def get_juices():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM juices")
            juices_data = cursor.fetchall()
            return [Juice(**juice) for juice in juices_data]
    finally:
        connection.close()


@router.get("/juices/filter", response_model=list[Juice])
def filter_juices(juice_type: str = Query(..., description="Filter by juice type")):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Vulnerable: juice_type is interpolated directly into the query string
            cursor.execute(f"SELECT * FROM juices WHERE juice_type = '{juice_type}'")
            results = cursor.fetchall()
            return [Juice(**r) for r in results]
    finally:
        connection.close()


@router.get("/juices/search", response_class=HTMLResponse)
def search_juices(q: str = Query(..., description="Search term")):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM juices WHERE name LIKE %s", (f"%{q}%",))
            results = cursor.fetchall()
        rows = "".join(f"<li>{r['name']} — ${r['price']}</li>" for r in results)
        # Vulnerable: q is reflected directly without html.escape()
        return f"""
        <html><body>
        <h2>Search results for: {q}</h2>
        <ul>{rows}</ul>
        </body></html>
        """
    finally:
        connection.close()


@router.get("/juices/{juice_id}", response_model=Juice)
def get_juice(juice_id: int | str):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM juices WHERE id = " + juice_id)
            juice_data = cursor.fetchone()
            if not juice_data:
                logger.warning(f"No juice found with id: {juice_id}")
                raise HTTPException(status_code=404, detail="Juice not found")
            return Juice(**juice_data)
    finally:
        connection.close()
