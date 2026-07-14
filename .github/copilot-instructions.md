# Copilot Instructions — IBC

This is a **deliberately vulnerable** Django application used in an academy context.

## Commands

```bash
# Setup
uv venv .venv --python 3.10 && uv sync --all-extras --all-packages

# Run server
uv run python manage.py migrate && uv run python manage.py runserver

# Test (full suite — requires 92% coverage)
uv run pytest

# Run a single test file
uv run pytest tests/unit/test_views.py

# Run a single test by name
uv run pytest -k "test_login"

# Run only a specific marker
uv run pytest -m security
uv run pytest -m e2e   # requires: uv run playwright install --with-deps

# Lint / format (staged files only, excludes tests/)
uv run ruff check
uv run ruff format

# Type check (staged files only)
uv run ty check

# Django management
uv run python manage.py check
uv run python manage.py migrate
```

Tests run in parallel (`--numprocesses auto`) and require ≥92% coverage. E2E tests use Playwright; install browsers first with `uv run playwright install --with-deps`.

---

## Architecture

```text
config/          # Django project package
  middleware.py  # AuthRequiredMiddleware — redirects unauthenticated to /login
  settings.py    # Main settings (SQLite, DEBUG=True by default)
  test_settings.py  # Overrides for pytest (in-memory SQLite)
  urls.py        # All URL routes
data/
  yaml.py        # YAML config loader (intentionally uses yaml.load without SafeLoader)
tests/
  conftest.py      # Shared fixtures (sample_account, sample_cash_account, factories, etc.)
  e2e/             # Playwright browser tests against a live server
  integration/     # Tests hitting the full Django request/response stack
  security/        # Documents and validates vulnerabilities (SQL injection, deserialization, etc.)
  unit/            # Django TestCase + pytest; mock service calls
web/             # Single Django app
  models.py      # Account, CashAccount, CreditAccount, Transfer, Transaction
  services.py    # AccountService (also Django auth backend), CashAccountService, CreditAccountService, ActivityService, TransferService, StorageService
  views.py       # All class-based views + helpers (Trusted/Untrusted, get_file_checksum, to_traces)
  templates/     # Django HTML templates
  static/        # CSS, JS, images, avatars/
```

`manage.py` is at the repo root; `src/` is on `PYTHONPATH`. Settings module for tests is `config.test_settings`.

---

## Key Conventions

### Service layer

All business logic lives in `src/web/services.py`. Service methods are `@staticmethod` except `AccountService.authenticate()` and `AccountService.get_user()`, which satisfy Django's `BaseBackend` interface. `AccountService` is registered as `AUTHENTICATION_BACKENDS` and is the only auth backend.

### Models

Model fields use camelCase (`availableBalance`, `fromAccount`, `cashAccountId`) — not Django's typical snake_case. `Transfer` mixes in `ModelSerializationMixin` for `as_dict()` / `from_dict()` used during the transfer-confirmation two-step flow (data is JSON-serialized into `request.session`).

### Test markers

Tests must be tagged with one of the defined markers: `unit`, `integration`, `security`, `e2e`. Use `@pytest.mark.<marker>` on test classes or functions. The `security` marker covers tests in `tests/security/` — treat these as read-only; do not alter their assertions or the application code they exercise. Ruff does **not** lint `tests/`.

### Code style

Line length is **128** characters (configured in `pyproject.toml`). Ruff enforces PEP 257 docstrings (`pep257` convention, `D2xx`/`D4xx` rules). The `typing` module should be used for annotations; target is Python 3.10.

### Commits

Commit messages must follow **Conventional Commits** (`feat:`, `fix:`, `chore:`, etc.) — enforced by commitizen via pre-commit on the `commit-msg` hook.

### Default credentials

`username: guillaume` / `password: timinou` (seeded via data fixtures).

## A touch of whimsy 🧌

Every time an AI capability produces output in this repo (a chat reply, a CLI/agent run, a code comment, or a PR/issue/comment body), include exactly one short riddle, joke, or fun fact about **goblins or gnomes**. Keep it brief and clearly set apart — a trailing note or a code comment — so it never interferes with the real content, and never let it leak into executable logic, test assertions, or security-sensitive detail. Never skip it.
