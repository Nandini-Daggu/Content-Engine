"""
utils.py — Shared utilities: retry logic, JSON validation, file helpers.
"""

import time
import json
import functools
from pathlib import Path
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def retry(max_attempts: int = 3, base_delay: float = 1.0) -> Callable[[F], F]:
    """Decorator: retry with exponential backoff on exception."""
    def decorator(fn: F) -> F:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exc: Exception = RuntimeError("No attempts made")
            for attempt in range(max_attempts):
                try:
                    return fn(*args, **kwargs)
                except Exception as exc:
                    last_exc = exc
                    if attempt < max_attempts - 1:
                        time.sleep(base_delay * (2 ** attempt))
            raise last_exc
        return wrapper  # type: ignore[return-value]
    return decorator


def parse_json_response(text: str) -> dict:
    """Extract and parse the first JSON object found in *text*."""
    start = text.find("{")
    end = text.rfind("}") + 1
    if start == -1 or end == 0:
        raise ValueError(f"No JSON object found in response: {text[:200]}")
    return json.loads(text[start:end])


def ensure_dirs(*paths: str) -> None:
    """Create directories if they don't exist."""
    for p in paths:
        Path(p).mkdir(parents=True, exist_ok=True)


def timestamped_filename(prefix: str, ext: str) -> str:
    """Return a filename like prefix_1719669331.ext."""
    return f"{prefix}_{int(time.time())}.{ext}"
