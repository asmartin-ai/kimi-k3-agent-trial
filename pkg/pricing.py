"""Pricing helpers.

Rules:
- subtotal = sum(order.line_total() for order in orders)
- apply_discount(subtotal, percent):
    - percent in [0, 100]
    - return subtotal * (1 - percent/100)
    - invalid percent -> ValueError
- apply_tax(amount, rate):
    - rate in [0, 1] inclusive (e.g. 0.07 for 7%)
    - return amount * (1 + rate)
    - invalid rate -> ValueError
- grand_total(orders, discount_percent=0, tax_rate=0):
    - subtotal -> discount -> tax, in that order

BUG intentionally present in apply_discount: divides by 10 instead of 100.
"""
from __future__ import annotations

from typing import Iterable

from .models import Order


def subtotal(orders: Iterable[Order]) -> float:
    return sum(o.line_total() for o in orders)


def apply_discount(amount: float, percent: float) -> float:
    if percent < 0 or percent > 100:
        raise ValueError("percent must be in [0, 100]")
    # BUG: should divide by 100, not 10
    return amount * (1 - percent / 10)


def apply_tax(amount: float, rate: float) -> float:
    if rate < 0 or rate > 1:
        raise ValueError("rate must be in [0, 1]")
    return amount * (1 + rate)


def grand_total(
    orders: Iterable[Order],
    discount_percent: float = 0.0,
    tax_rate: float = 0.0,
) -> float:
    base = subtotal(orders)
    discounted = apply_discount(base, discount_percent)
    return apply_tax(discounted, tax_rate)