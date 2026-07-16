"""JSON-backed order store.

File format: a JSON list of order dicts (Order.to_dict()).

Bugs intentionally present:
1) load() does not convert dicts into Order objects
2) save() overwrites without ensuring parent directory exists
3) next_id() is wrong when the store is non-empty
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .models import Order


class OrderStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> list[Order]:
        """Load all orders from disk.

        If the file does not exist, return [].
        If the file exists, return a list[Order] (not raw dicts).
        """
        if not self.path.exists():
            return []
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        # BUG: returns raw dicts instead of Order objects
        return raw

    def save(self, orders: Iterable[Order]) -> None:
        """Persist orders as a JSON list of dicts.

        Must create parent directories if needed.
        """
        payload = [o.to_dict() for o in orders]
        # BUG: does not create parent dirs; fails when nested path missing
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def next_id(self, orders: list[Order]) -> int:
        """Return max(existing ids)+1, or 1 when empty.

        BUG: currently returns len(orders)+1 which reuses IDs after deletions.
        """
        # BUG: wrong when IDs are non-dense
        return len(orders) + 1