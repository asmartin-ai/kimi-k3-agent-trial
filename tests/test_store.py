from pathlib import Path

from pkg.models import Order, OrderStatus
from pkg.store import OrderStore


def test_load_missing_file_returns_empty(tmp_path: Path):
    store = OrderStore(tmp_path / "nope.json")
    assert store.load() == []


def test_save_and_load_roundtrip(tmp_path: Path):
    path = tmp_path / "nested" / "orders.json"
    store = OrderStore(path)
    orders = [
        Order(id=1, sku="A", quantity=1, unit_price=5.0, status=OrderStatus.PENDING),
        Order(id=2, sku="B", quantity=2, unit_price=3.0, status=OrderStatus.PAID),
    ]
    store.save(orders)
    loaded = store.load()
    assert loaded == orders
    assert all(isinstance(o, Order) for o in loaded)


def test_next_id_handles_gaps():
    store = OrderStore("unused.json")
    orders = [
        Order(id=1, sku="A", quantity=1, unit_price=1.0),
        Order(id=5, sku="B", quantity=1, unit_price=1.0),
    ]
    assert store.next_id(orders) == 6
    assert store.next_id([]) == 1
