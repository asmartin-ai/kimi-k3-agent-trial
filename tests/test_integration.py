from pathlib import Path

from pkg.models import OrderStatus
from pkg.pricing import grand_total
from pkg.service import OrderService
from pkg.store import OrderStore


def test_end_to_end_order_desk(tmp_path: Path):
    store = OrderStore(tmp_path / "data" / "orders.json")
    svc = OrderService(store)

    a = svc.add_order("WIDGET", 2, 25.0)  # 50
    b = svc.add_order("GADGET", 1, 40.0)  # 40
    svc.pay(a.id)
    svc.ship(a.id)
    svc.pay(b.id)

    assert svc.revenue() == 90.0

    # reload from disk through a new service instance
    svc2 = OrderService(OrderStore(tmp_path / "data" / "orders.json"))
    orders = svc2.list_orders()
    assert len(orders) == 2
    assert {o.status for o in orders} == {OrderStatus.SHIPPED, OrderStatus.PAID}

    # 10% discount then 0% tax on all current orders
    assert grand_total(orders, discount_percent=10, tax_rate=0.0) == 81.0
