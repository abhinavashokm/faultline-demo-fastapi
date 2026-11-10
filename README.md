# Chaos shop

A standalone FastAPI demo app with endpoints that misbehave on purpose.

## Quick start

1. Install dependencies:
   ```bash
   pip install fastapi uvicorn
   ```

2. Start the server:
   ```bash
   uvicorn chaos_shop:app --port 8000
   ```

3. Open your browser:
   ```
   http://localhost:8000
   ```

## Where to add your own setup

In `chaos_shop.py`, you will find specific placeholders and helper functions:

### Setup placeholders
- `# ===== SETUP (I will add this myself): startup code goes here, inside the lifespan before `yield` =====`
  Inside the lifespan context manager before `yield` for any startup initialization logic.
- `# ===== SETUP (I will add this myself): middleware for `app` goes here =====`
  Immediately after creating `app = FastAPI(lifespan=lifespan)` for registering custom middleware on `app`.
- `# ===== SETUP (I will add this myself): shutdown code goes here, inside the lifespan after `yield` =====`
  Inside the lifespan context manager after `yield` for any cleanup or shutdown logic.

### Reporting helpers
- `report_exception(exc: BaseException, context: dict | None = None) -> str | None`
  Called by endpoints when an exception is caught. Custom error reporting or dispatching logic can be inserted here.
- `report_message(message: str, level: str = "warning") -> str | None`
  Called by endpoints to report custom warning or informational messages.
