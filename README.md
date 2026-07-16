# Kimi K3 Agentic Trial

Multi-file coding trial for evaluating **Kimi K3** (or any agent) on a realistic mini-codebase.

This is intentionally harder than a single-function chat puzzle:
- multiple modules
- a real bug + incomplete features
- tests that fail until the agent fixes the right places
- constraints against rewriting the whole project

## Quick start

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

Expected on a clean checkout: **tests fail**.

When the agent is done, the same command should pass.

## Layout

```
pkg/
  models.py      # data models (partially implemented)
  store.py       # JSON persistence (buggy)
  service.py     # business logic (incomplete)
  pricing.py     # pricing helpers (buggy)
  __init__.py
tests/
  test_models.py
  test_store.py
  test_service.py
  test_pricing.py
  test_integration.py
PROMPT_FOR_KIMI.md   # paste this into Kimi K3 after connecting GitHub
```

## Success criteria

All of these must be true:

1. `python -m pytest -q` exits 0
2. No test files modified
3. Minimal, surgical production changes only
4. Existing public function signatures preserved

## License

MIT — trial/eval fixture only.