"""Order data model.

Rules:
- Order IDs are positive ints assigned by the service/store layer.
- SKU is a non-empty stripped string.
- Quantity is a positive int (>= 1).
- Unit price is a non-negative float.
- Status transitions are controlled by OrderService, not callers.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class OrderStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"


@dataclass
class Order:
    id: int
    sku: str
    quantity: int
    unit_price: float
    status: OrderStatus = OrderStatus.PENDING

    def line_total(self) -> float:
        """Return quantity * unit_price.

        Must be exact for the values used in tests (no rounding tricks required).
        """
        raise NotImplementedError

    def to_dict(self) -> dict[str, Any]:
        """Serialize for JSON storage.

        Required shape:
        {
          "id": int,
          "sku": str,
          "quantity": int,
          "unit_price": float,
          "status": str  # enum value, e.g. "pending"
        }
        """
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Order":
        """Deserialize from JSON storage.

        Must accept the shape produced by to_dict().
        Invalid/missing fields should raise ValueError or KeyError naturally.
        """
        raise NotImplementedError


def validate_new_order_fields(sku: str, quantity: int, unit_price: float) -> tuple[str, int, float]:
    """Normalize and validate fields for a new order.

    - sku: strip whitespace; empty after strip -> ValueError
    - quantity: must be int >= 1; otherwise ValueError
    - unit_price: must be >= 0; otherwise ValueError
    Returns normalized (sku, quantity, unit_price).
    """
    raise NotImplementedError