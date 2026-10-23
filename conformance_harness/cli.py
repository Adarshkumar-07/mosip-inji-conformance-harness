"""Command-line entry point for per-component and combined runs."""
import argparse
import json
from pathlib import Path
from .runner import run_component

def main() -> int:
    parser = argparse.ArgumentParser(description="Run Inji OpenID conformance automation")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--component", choices=("certify", "verify"))
    group.add_argument("--combined", action="store_true")
    parser.add_argument("--config-dir", type=Path, default=Path("config"))
    parser.add_argument("--output", type=Path, help="Optional path to write normalized JSON results")
    args = parser.parse_args()
    components = ["certify", "verify"] if args.combined else [args.component]
    results = [run_component(name, args.config_dir / f"{name}.json") for name in components]
    payload = {"runs": [r.to_dict() for r in results], "overall_status": "PASS" if all(r.status == "PASS" for r in results) else "FAIL"}
    rendered = json.dumps(payload, indent=2)
    print(rendered)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    # Scaffold is not a conformance pass: any status other than PASS fails closed.
    return 0 if payload["overall_status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
