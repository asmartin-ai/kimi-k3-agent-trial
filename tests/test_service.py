from pathlib import Path

import pytest

from pkg.models import OrderStatus
from pkg.service import OrderService
from pkg.store import OrderStore


@pytest.fixture
def svc(tmp_path: Path) -> OrderService:
    return OrderService(OrderStore(tmp_path / "orders.json"))


def test_add_and_get(svc: OrderService):
    o = svc.add_order("SKU", 2, 4.0)
    assert o.id == 1
    assert o.status == OrderStatus.PENDING
    assert svc.get_order(1) == o


def test_list_filter(svc: OrderService):
    svc.add_order("A", 1, 1.0)
    b = svc.add_order("B", 1, 1.0)
    svc.pay(b.id)
    pending = svc.list_orders(OrderStatus.PENDING)
    paid = svc.list_orders(OrderStatus.PAID)
    assert [o.sku for o in pending] == ["A"]
    assert [o.sku for o in paid] == ["B"]


def test_status_transitions(svc: OrderService):
    o = svc.add_order("A", 1, 10.0)
    paid = svc.pay(o.id)
    assert paid.status == OrderStatus.PAID
    shipped = svc.ship(o.id)
    assert shipped.status == OrderStatus.SHIPPED
    with pytest.raises(ValueError):
        svc.cancel(o.id)


def test_cancel_pending(svc: OrderService):
    o = svc.add_order("A", 1, 10.0)
    c = svc.cancel(o.id)
    assert c.status == OrderStatus.CANCELLED


def test_pay_wrong_status(svc: OrderService):
    o = svc.add_order("A", 1, 10.0)
    svc.pay(o.id)
    with pytest.raises(ValueError):
        svc.pay(o.id)


def test_revenue_ignores_pending_and_cancelled(svc: OrderService):
    a = svc.add_order("A", 2, 5.0)  # 10 pending
    b = svc.add_order("B", 1, 7.0)  # 7 -> paid
    c = svc.add_order("C", 3, 3.0)  # 9 -> paid -> shipped
    d = svc.add_order("D", 1, 100.0)  # cancelled
    svc.pay(b.id)
    svc.pay(c.id)
    svc.ship(c.id)
    svc.cancel(d.id)
    # paid(7) + shipped(9) = 16; pending/cancelled excluded
    assert svc.revenue() == 16.0
    assert svc.get_order(a.id).status == OrderStatus.PENDING
