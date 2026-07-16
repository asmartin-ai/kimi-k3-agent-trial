import pytest

from pkg.models import Order, OrderStatus, validate_new_order_fields


def test_line_total():
    o = Order(id=1, sku="ABC", quantity=3, unit_price=2.5)
    assert o.line_total() == 7.5


def test_to_from_dict_roundtrip():
    o = Order(id=7, sku="SKU-1", quantity=2, unit_price=10.0, status=OrderStatus.PAID)
    d = o.to_dict()
    assert d == {
        "id": 7,
        "sku": "SKU-1",
        "quantity": 2,
        "unit_price": 10.0,
        "status": "paid",
    }
    o2 = Order.from_dict(d)
    assert o2 == o


def test_validate_new_order_fields_ok():
    assert validate_new_order_fields("  abc  ", 2, 0.0) == ("abc", 2, 0.0)


def test_validate_new_order_fields_rejects():
    with pytest.raises(ValueError):
        validate_new_order_fields("   ", 1, 1.0)
    with pytest.raises(ValueError):
        validate_new_order_fields("x", 0, 1.0)
    with pytest.raises(ValueError):
        validate_new_order_fields("x", 1, -0.01)
