"""Order service / business logic.

Required behavior:
- add_order(sku, quantity, unit_price) -> Order
- get_order(order_id) -> Order  (KeyError if missing)
- list_orders(status: OrderStatus | None = None) -> list[Order]
- pay(order_id) -> Order
- ship(order_id) -> Order
- cancel(order_id) -> Order
- revenue() -> float  (sum of line totals for PAID + SHIPPED only)

Status rules:
- new orders start PENDING
- pay: PENDING -> PAID; otherwise ValueError
- ship: PAID -> SHIPPED; otherwise ValueError
- cancel: PENDING or PAID -> CANCELLED; SHIPPED cannot cancel -> ValueError
"""
from __future__ import annotations

from .models import Order, OrderStatus, validate_new_order_fields
from .store import OrderStore


class OrderService:
    def __init__(self, store: OrderStore):
        self.store = store

    def _all(self) -> list[Order]:
        return self.store.load()

    def _write(self, orders: list[Order]) -> None:
        self.store.save(orders)

    def add_order(self, sku: str, quantity: int, unit_price: float) -> Order:
        """Create and persist a new PENDING order with the next id."""
        raise NotImplementedError

    def get_order(self, order_id: int) -> Order:
        raise NotImplementedError

    def list_orders(self, status: OrderStatus | None = None) -> list[Order]:
        """Return all orders, optionally filtered by status.

        Preserve stable order as stored.
        """
        raise NotImplementedError

    def pay(self, order_id: int) -> Order:
        raise NotImplementedError

    def ship(self, order_id: int) -> Order:
        raise NotImplementedError

    def cancel(self, order_id: int) -> Order:
        raise NotImplementedError

    def revenue(self) -> float:
        """Sum line totals for PAID and SHIPPED orders only."""
        raise NotImplementedError