"""Normalized result structures used by CLI and future TestNG bridge."""
from dataclasses import asdict, dataclass, field
from typing import Any, Literal

Status = Literal["PASS", "FAIL", "SKIP", "ERROR", "RUNNING", "UNKNOWN"]

@dataclass
class TestResult:
    name: str
    status: Status
    message: str = ""
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class RunResult:
    component: str
    status: Status
    execution_id: str | None = None
    tests: list[TestResult] = field(default_factory=list)
    message: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
