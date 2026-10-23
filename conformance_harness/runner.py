"""Orchestrate one configured component without assuming undocumented API routes."""
import json
from pathlib import Path
from typing import Any
from .client import ConformanceApiClient, ConformanceApiError
from .results import RunResult

class ConfigurationError(ValueError):
    """Raised when a component configuration is missing required verified values."""

def load_config(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ConfigurationError(f"Configuration not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ConfigurationError(f"Invalid JSON configuration: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ConfigurationError("Configuration root must be a JSON object.")
    return data

def run_component(component: str, config_path: Path) -> RunResult:
    config = load_config(config_path)
    base_url = config.get("conformance_base_url")
    routes = config.get("routes", {})
    if not base_url:
        return RunResult(component, "ERROR", message="Set conformance_base_url after the local suite URL is verified.")
    required = ("create", "configure", "start", "status", "results")
    missing = [name for name in required if not isinstance(routes.get(name), dict) or not routes[name].get("path")]
    if missing:
        return RunResult(component, "ERROR", message="Verified API route configuration missing: " + ", ".join(missing))
    # The route templates and payloads must be filled from the official API docs.
    # The concrete execution protocol is intentionally not guessed in this scaffold.
    client = ConformanceApiClient(base_url, int(config.get("timeout_seconds", 30)))
    try:
        # First request is a reachability check against a documented, configured route.
        probe = routes.get("health")
        if probe and probe.get("path"):
            client.request(probe.get("method", "GET"), probe["path"])
        return RunResult(component, "SKIP", message="API routes are configured; plan lifecycle adapter still needs verified request/response mappings.")
    except (ConformanceApiError, ValueError) as exc:
        return RunResult(component, "ERROR", message=str(exc))
