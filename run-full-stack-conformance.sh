#!/usr/bin/env bash
set -euo pipefail

# This wrapper currently invokes the Python scaffold. Full Docker and TestNG
# orchestration will be added after service/API contracts are verified.
exec python -m conformance_harness.cli "$@"
