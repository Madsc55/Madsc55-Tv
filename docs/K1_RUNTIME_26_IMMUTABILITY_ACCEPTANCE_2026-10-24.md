# K1 runtime 26 / protected-file immutability — evidence boundary

The main task ledger currently reports K1-01 and K1-02 pending and runtime acceptance 0/26. This change does **not** change those statuses.

- `madsc/k1_runtime_26_evidence.py` creates a fail-closed 26-slot observation report. Rule identifiers are placeholders until mapped to the actual 26 policy definitions. An observation with `runtime_executed` and an evidence string is still a caller claim; it is never independently accepted automatically.
- `madsc/k1_immutability_evidence.py` compares protected file bytes (SHA-256), metadata, inode and device before/after an isolated run. It cannot prove that a file was never transiently changed and restored, nor can it detect effects outside the supplied paths.
- Runtime acceptance requires independently observed deny/allow behavior for each actual policy rule, sandboxed execution with protected production data inaccessible, externally preserved test logs, and independently checked baseline/final protected-file manifests.
- No actual 26-rule runtime execution, production file snapshot, or GitHub CI success has been verified in this PR. Do not mark K1-01 or K1-02 accepted.
