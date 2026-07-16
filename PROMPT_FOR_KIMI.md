# Paste this into Kimi K3 after it has GitHub access to this repo

You have access to the GitHub repository for this project (kimi-k3-agent-trial).  
You do **not** need me to paste file contents — open the repo and inspect it yourself.

## Mission

Make the test suite pass with **surgical production-code fixes only**.

## Hard constraints

1. **Do not modify any files under `tests/`.**
2. Preserve public function/class signatures in `pkg/`.
3. Prefer minimal diffs over rewrites.
4. Do not add new dependencies beyond `pytest` already listed.
5. When finished, `python -m pytest -q` must exit 0.

## Suggested workflow

1. Clone/open this repo.
2. Install deps: `python -m pip install -r requirements.txt`
3. Run: `python -m pytest -q` and read failures.
4. Inspect:
   - `pkg/models.py`
   - `pkg/store.py`
   - `pkg/service.py`
   - `pkg/pricing.py`
5. Implement missing pieces and fix intentional bugs.
6. Re-run tests until green.
7. Summarize:
   - files changed
   - bugs fixed
   - final pytest result

## Domain summary

Mini order desk:

- `Order` model with serialization + validation helpers
- `OrderStore` JSON persistence (has real bugs)
- `OrderService` business logic/status transitions (mostly unimplemented)
- `pricing` helpers (one intentional discount bug)

Status rules for service:

- new orders: `PENDING`
- `pay`: `PENDING -> PAID` else `ValueError`
- `ship`: `PAID -> SHIPPED` else `ValueError`
- `cancel`: `PENDING|PAID -> CANCELLED`; cannot cancel `SHIPPED`
- `revenue`: sum of line totals for `PAID` + `SHIPPED` only

## Done when

- all tests pass
- tests directory untouched
- you report the final pytest summary and a short change list
