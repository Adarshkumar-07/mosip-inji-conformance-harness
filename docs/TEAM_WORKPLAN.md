# Team work plan — MOSIP Decode

## Member A — Python runner
- Own `conformance_harness/` and `tests/`.
- Verify the OpenID REST API routes and request/response formats from the official docs.
- Implement create/configure/start/poll/results only after confirming exact API contracts.
- Add tests for success, API failure, timeout, invalid response and per-test status mapping.

## Member B — laptop / environment and test-rig integration
- Inspect the target Inji Certify and Inji Verify 1.0.x setup and MOSIP functional-test modules.
- Verify Docker Compose dependencies, endpoint URLs, aliases and variants.
- Own Docker Compose and the Java TestNG integration, keeping each module's suite separate.
- Record real end-to-end execution evidence and blockers.

## Member C — quality, CI and submission artefacts
- Own CI workflow, README review, architecture diagram, test matrix and demo plan.
- Confirm the CI command and expected exit status with Member A and Member B.
- Prepare pitch slides, 2–5 minute demo video, test data notes, and collect all three college IDs.
- Keep a checklist of what is actually implemented versus planned.

## Integration contract
- CLI modes: `--component certify`, `--component verify`, `--combined`.
- JSON result fields: `component`, `status`, `execution_id`, `tests`, `message`.
- Exit 0 only when every required real conformance run passes; errors, skips, or unknown outcomes must not be reported as conformance success.
- Do not commit secrets or claim real conformance based only on mocks.

## Deadline checkpoints
- 23 Oct: API contract, service topology, branch ownership agreed.
- 24 Oct: runner lifecycle and configuration tested; first integration attempt.
- 25 Oct: merged candidate, test evidence, README, pitch/video ready.
- 26 Oct: final link/access check and submission.
