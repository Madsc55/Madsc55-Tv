# K2 daily evidence: operational acceptance boundaries

The offline function `build_daily_evidence` creates a deterministic candidate snapshot and change report. It does **not** schedule itself, access the network, authenticate a broadcaster, verify a license, or attest to GitHub Actions execution.

The `source_commit` parameter is a caller-supplied reference and is syntactically validated only. `artifact_sha256` detects accidental or adversarial modification only when compared to a separately trusted copy of the expected digest. It is not a signature, trusted timestamp, GitHub run attestation, or proof of origin.

To activate daily operation safely: run a reviewed, read-only scheduled workflow; pin the input source registry to approved official domains; persist each day's JSON as an immutable CI artifact; record the real workflow run ID, commit and artifact digest from the runner; verify provenance against GitHub's attestation API or a separately trusted signed manifest. Require manual review for removed feeds and never auto-publish candidates.

Real rights verification requires documentary permission from the rights holder or an authoritative published license explicitly covering the intended stream use and territory, with a dated source and reviewer. A web page, M3U URL, or boolean assertion is not sufficient. All candidates remain REVIEW_REQUIRED.

No live probing, production playlist writes, workflow dispatch, secrets changes, or PR merge were performed.

## Proposed daily workflow (not yet active)

`.github/workflows/k2-daily-discovery.yml` schedules an offline report at 04:23 UTC daily, once this workflow is present on the default branch. The initial registry is an empty JSON array; consequently no actual broadcaster is currently verified. A successful empty-registry run would only prove that the reporting pipeline executed.

The runner records `GITHUB_SHA`, `GITHUB_RUN_ID`, `GITHUB_RUN_ATTEMPT`, repository and workflow ref as **untrusted context claims** inside the JSON. The SHA-256 sidecar supports independent byte comparison but is not cryptographic identity proof. Real provenance acceptance requires verifying the workflow run and artifact via GitHub's API, matching commit and run attempt, and obtaining/verifying a trusted artifact attestation or signed manifest.

Do not add source entries until their authoritative rights documentation has been manually reviewed. Do not merge or manually dispatch without the project's normal approval and CI process.
