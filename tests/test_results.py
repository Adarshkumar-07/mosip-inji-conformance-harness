import json
from conformance_harness.results import RunResult, TestResult
from conformance_harness.runner import load_config, ConfigurationError

def test_result_serializes_for_reports():
    result = RunResult("certify", "PASS", execution_id="abc", tests=[TestResult("issuer-check", "PASS")])
    data = result.to_dict()
    assert data["component"] == "certify"
    assert data["tests"][0]["status"] == "PASS"

def test_load_config_rejects_non_object(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text(json.dumps(["not", "object"]), encoding="utf-8")
    try:
        load_config(path)
    except ConfigurationError as exc:
        assert "JSON object" in str(exc)
    else:
        raise AssertionError("Expected ConfigurationError")

def test_missing_config_is_clear(tmp_path):
    try:
        load_config(tmp_path / "missing.json")
    except ConfigurationError as exc:
        assert "not found" in str(exc)
    else:
        raise AssertionError("Expected ConfigurationError")
