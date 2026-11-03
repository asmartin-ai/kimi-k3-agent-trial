# Agent coding trial

A small multi-file coding benchmark originally written for Kimi K3. It can also
be used with another coding agent. The repository is an evaluation fixture,
not a finished application: its bugs and incomplete features are intentional.

Tests fail on a clean checkout by design; the task is to make them pass without
changing the tests or rewriting the project.

## Quick start

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

Expected on a clean checkout: **tests fail**.

When the agent is done, the same command should pass.

Give the agent [PROMPT_FOR_KIMI.md](PROMPT_FOR_KIMI.md), which describes the
task and constraints. The prompt names Kimi K3 but the trial is not limited to
that model.

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
PROMPT_FOR_KIMI.md   # agent task and constraints
```

## Success criteria

All of these must be true:

1. `python -m pytest -q` exits 0
2. No test files modified
3. Minimal, surgical production changes only
4. Existing public function signatures preserved

## License

MIT — trial/eval fixture only.