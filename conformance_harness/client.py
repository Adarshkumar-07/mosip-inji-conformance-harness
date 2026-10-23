"""Small standard-library HTTP client; endpoint paths come from verified config.

Do not hard-code OpenID suite routes here. Populate routes only after confirming
those routes and payloads in the suite's current REST API documentation.
"""
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from typing import Any

class ConformanceApiError(RuntimeError):
    """Raised for transport errors, HTTP failures, or invalid JSON responses."""

class ConformanceApiClient:
    def __init__(self, base_url: str, timeout_seconds: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def request(self, method: str, path: str, payload: dict[str, Any] | None = None) -> Any:
        if not path or not path.startswith("/"):
            raise ValueError("API path must be an absolute path beginning with '/'.")
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        headers = {"Accept": "application/json"}
        if body is not None:
            headers["Content-Type"] = "application/json"
        req = Request(f"{self.base_url}{path}", data=body, headers=headers, method=method.upper())
        try:
            with urlopen(req, timeout=self.timeout_seconds) as response:
                raw = response.read().decode("utf-8")
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ConformanceApiError(f"HTTP {exc.code} for {method} {path}: {detail}") from exc
        except (URLError, TimeoutError) as exc:
            raise ConformanceApiError(f"Request failed for {method} {path}: {exc}") from exc
        if not raw.strip():
            return {}
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ConformanceApiError(f"Expected JSON from {method} {path}") from exc
