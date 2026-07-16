import pytest

from pkg.models import Order, OrderStatus
from pkg.pricing import apply_discount, apply_tax, grand_total, subtotal


def test_subtotal():
    orders = [
        Order(id=1, sku="A", quantity=2, unit_price=5.0),
        Order(id=2, sku="B", quantity=1, unit_price=3.0),
    ]
    # depends on Order.line_total implementation
    assert subtotal(orders) == 13.0


def test_discount_and_tax():
    assert apply_discount(100.0, 10) == 90.0
    assert apply_tax(90.0, 0.1) == 99.0


def test_discount_invalid():
    with pytest.raises(ValueError):
        apply_discount(10, -1)
    with pytest.raises(ValueError):
        apply_discount(10, 101)


def test_tax_invalid():
    with pytest.raises(ValueError):
        apply_tax(10, -0.01)
    with pytest.raises(ValueError):
        apply_tax(10, 1.01)


def test_grand_total_order():
    orders = [Order(id=1, sku="A", quantity=2, unit_price=50.0, status=OrderStatus.PAID)]
    # subtotal 100, 10% off -> 90, 10% tax -> 99
    assert grand_total(orders, discount_percent=10, tax_rate=0.1) == 99.0
