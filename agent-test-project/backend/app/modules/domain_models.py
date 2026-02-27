from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel


class JuiceType(StrEnum):
    ORANGE = "orange"
    APPLE = "apple"


class Juice(BaseModel):
    id: int
    name: str
    description: str | None = None
    juice_type: JuiceType
    price: Decimal
    in_stock: bool = True


class CreateJuiceRequest(BaseModel):
    name: str
    description: str | None = None
    juice_type: JuiceType
    price: Decimal
    in_stock: bool = True


class UpdateJuiceRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    juice_type: JuiceType | None = None
    price: Decimal | None = None
    in_stock: bool | None = None
