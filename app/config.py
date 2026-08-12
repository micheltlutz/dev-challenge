"""Application settings.

Values come from the environment (optionally via an ``app/.env`` file, which is
NOT tracked in git). Every setting has a lab-friendly default so the project
boots with zero configuration -- ``docker run`` and ``uvicorn app.main:app``
both work on a fresh clone.

The one exception is ``SECRET``: when it is absent we generate a random,
process-local key instead of falling back to a hard-coded one. That keeps
tokens working for a local lab session while making it impossible to ship a
publicly known JWT signing key.
"""

import logging
import os
import secrets
from pathlib import Path

from dotenv import load_dotenv

# Resolve the .env explicitly. A bare load_dotenv() searches upward from the
# current working directory, so running `uvicorn app.main:app` from the repo
# root silently missed app/.env entirely.
_APP_DIR = Path(__file__).resolve().parent
for _candidate in (_APP_DIR / ".env", _APP_DIR.parent / ".env"):
    if _candidate.is_file():
        load_dotenv(_candidate)
        break

logger = logging.getLogger(__name__)


def _int_env(name: str, default: int) -> int:
    """Read an int setting, tolerating the ``30 # comment`` style used in .env."""
    raw = os.getenv(name)
    if raw is None:
        return default
    raw = raw.split("#", 1)[0].strip()
    try:
        return int(raw)
    except ValueError:
        logger.warning("Invalid int for %s=%r, falling back to %s", name, raw, default)
        return default


def _resolve_secret() -> str:
    configured = os.getenv("SECRET")
    if configured:
        return configured
    logger.warning(
        "SECRET is not set; generated an ephemeral one for this process. "
        "Tokens will not survive a restart. Set SECRET in app/.env "
        "(see app/.env.example) or as a deployment secret."
    )
    return secrets.token_hex(32)


APP_ENV = os.getenv("APP_ENV", "local")
PROJECT_NAME = os.getenv("PROJECT_NAME", "Development challenge")
VERSION = os.getenv("VERSION", "2.0.0")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

SECRET = _resolve_secret()
ALGORITHM = os.getenv("ALGORITHM", "HS256")
TOKEN_EXPIRES = _int_env("TOKEN_EXPIRES", 30)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev-challenge.db")

# Comma-separated list of allowed origins. The default is permissive because
# challengers run their front-ends on arbitrary localhost ports; a real
# deployment should pin this.
CORS_ALLOW_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ALLOW_ORIGINS", "*").split(",")
    if origin.strip()
]

# Echoing every SQL statement is useful while studying the reference
# implementation, but it is noise in CI and in the hosted instance.
SQL_ECHO = os.getenv("SQL_ECHO", "false").lower() in {"1", "true", "yes"}
