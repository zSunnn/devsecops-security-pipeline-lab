Finding: ZAP rule 10021 identified a missing X-Content-Type-Options header on / and /welcome.
Fix: Added X-Content-Type-Options: nosniff using Flask’s after_request hook.
Evidence: All three tests passed, curl confirmed the header was present, and the new ZAP report no longer contained finding 10021.
Limitations: Other alerts remain. Resolving one finding does not prove that the entire application is secure.

## CI DAST gate verification

The CI workflow builds the application image, starts Flask, waits
for an HTTP response, and runs ZAP Baseline. HTML and JSON reports
are uploaded even when the scan fails.

### Experiment

PR #5 temporarily configured the existing CSP finding (10038)
as FAIL.

Observed results:
- ZAP reported finding 10038 as FAIL and exited with code 1.
- The required CI check failed and GitHub blocked merging.
- Both HTML and JSON reports were uploaded.
- Reverting the temporary configuration restored a passing CI check.

Evidence: https://github.com/zSunnn/devsecops-security-pipeline-lab/pull/5

### Interpretation and limitations

This experiment verified that a ZAP finding configured as FAIL
can block merging. It did not fix the missing CSP header.

Rule 10021 remains configured as FAIL. Its finding was absent
after adding the nosniff header, but this experiment did not
specifically test a regression of rule 10021.

Other warnings remain. The -I option prevents WARN findings
from failing the scan; it does not suppress FAIL findings.

The upload step uses if-no-files-found: error. This fails when
no report files match, but does not independently guarantee
that both expected reports exist.