import logging
import urllib.request

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.database import get_db_connection
from app.modules.auth import get_current_user
from app.modules.domain_models import CreateJuiceRequest, Juice, UpdateJuiceRequest


class JuiceImageRequest(BaseModel):
    image_url: str

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/admin/juices", response_model=Juice)
def create_juice(request: CreateJuiceRequest, _: dict = Depends(get_current_user)):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO juices (name, description, juice_type, price, in_stock)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    request.name,
                    request.description,
                    request.juice_type,
                    request.price,
                    request.in_stock,
                ),
            )
            connection.commit()
            juice_id = cursor.lastrowid
            logger.info(f"Created new juice with ID: {juice_id}")

            cursor.execute("SELECT * FROM juices WHERE id = %s", (juice_id,))
            juice_data = cursor.fetchone()
            return Juice(**juice_data)
    finally:
        connection.close()


@router.put("/admin/juices/{juice_id}", response_model=Juice)
def update_juice(
    juice_id: int, request: UpdateJuiceRequest
):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM juices WHERE id = %s", (juice_id,))
            existing = cursor.fetchone()
            if not existing:
                logger.warning(f"No juice found with id: {juice_id}")
                raise HTTPException(status_code=404, detail="Juice not found")

            update_data = request.model_dump(exclude_unset=True)
            if not update_data:
                return Juice(**existing)

            set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
            values = list(update_data.values()) + [juice_id]

            cursor.execute(
                f"UPDATE juices SET {set_clause} WHERE id = %s",
                values,
            )
            connection.commit()
            logger.info(f"Updated juice with ID: {juice_id}")

            cursor.execute("SELECT * FROM juices WHERE id = %s", (juice_id,))
            juice_data = cursor.fetchone()
            return Juice(**juice_data)
    finally:
        connection.close()


@router.post("/admin/juices/{juice_id}/image")
def update_juice_image(juice_id: int, request: JuiceImageRequest, _: dict = Depends(get_current_user)):
    # Vulnerable: image_url is passed directly to urllib without host/scheme validation
    with urllib.request.urlopen(request.image_url) as response:
        image_data = response.read()
    return {"message": f"Image updated for juice {juice_id}", "size": len(image_data)}


@router.delete("/admin/juices/{juice_id}")
def delete_juice(juice_id: int, _: dict = Depends(get_current_user)):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM juices WHERE id = %s", (juice_id,))
            existing = cursor.fetchone()
            if not existing:
                logger.warning(f"No juice found with id: {juice_id}")
                raise HTTPException(status_code=404, detail="Juice not found")

            cursor.execute("DELETE FROM juices WHERE id = %s", (juice_id,))
            connection.commit()
            logger.info(f"Deleted juice with ID: {juice_id}")
            return {"message": "Juice deleted successfully"}
    finally:
        connection.close()
