# DevSecOps Security Pipeline Lab

A learning project covering Git, a small web application, automated tests,
SAST, DAST and GitHub Actions.

## Implemented features

- Flask application with automated pytest tests.
- Bandit SAST checks in GitHub Actions.
- Docker image build and application startup in CI.
- HTTP readiness check before DAST.
- ZAP Baseline scan with HTML and JSON report artifacts.
- Security gate: ZAP rule 10021 is configured as FAIL.
- Required CI check that blocks merging when it fails.

## Verified results

- Fixed missing X-Content-Type-Options by adding nosniff.
- Confirmed the header with pytest, curl and a follow-up ZAP scan.
- Temporarily configured existing CSP finding 10038 as FAIL:
  ZAP exited with code 1, CI failed, and GitHub blocked merging.
- Confirmed reports were uploaded despite the failed scan.
- Reverted the temporary policy and confirmed CI passed again.
  The missing CSP header remains unresolved.

See [SAST notes](docs/sast-lab.md),
[DAST notes](docs/dast-lab.md), and
[the gate verification PR](https://github.com/zSunnn/devsecops-security-pipeline-lab/pull/5).

## CI workflow

Pull request to main
→ Checkout and Python setup
→ Install dependencies
→ Pytest
→ Bandit
→ Build Docker image
→ Start Flask
→ Wait for HTTP readiness
→ ZAP Baseline
→ Upload reports, including when earlier steps fail

The workflow also runs on pushes to main.

## Run locally — Windows PowerShell

Prerequisites:
- Git and Python 3.13.
- Docker Desktop running with Linux containers.

Run the following commands from the repository root.

### Install dependencies and run checks

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m bandit app.py
```

If `.venv` already exists with Python 3.13, skip its creation.

### Build and start the application

```powershell
docker build -t devsecops-lab:local .
docker network create devsecops-net
docker run --rm --name devsecops-web --network devsecops-net -p 127.0.0.1:5000:5000 devsecops-lab:local
```

Create the network only once; reuse it if it already exists.
The container name `devsecops-web` must not already be in use.

The last command keeps the terminal attached to Flask.
Leave it running and open another PowerShell terminal to check:

```powershell
curl.exe -i http://127.0.0.1:5000/welcome
```

Expected: HTTP 200, the welcome message, and
`X-Content-Type-Options: nosniff`.

### Run ZAP Baseline

Keep the Flask container running. In a second PowerShell
terminal, run these commands from the repository root:

```powershell
New-Item -ItemType Directory -Force reports/raw
Copy-Item .zap/baseline.conf reports/raw/baseline.conf
$zapReportPath = (Resolve-Path reports/raw).Path

docker run --rm --network devsecops-net --mount "type=bind,source=$zapReportPath,target=/zap/wrk" ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t http://devsecops-web:5000/welcome -c baseline.conf -I -r zap-local.html -J zap-local.json

$LASTEXITCODE
```

The bind mount maps the local reports/raw directory to
/zap/wrk inside the ZAP container. ZAP reads baseline.conf
and writes its reports through that shared directory.

ZAP reaches Flask using the container name devsecops-web
and port 5000 on the shared Docker network.

Reports:
- reports/raw/zap-local.html
- reports/raw/zap-local.json

With -I, WARN findings do not cause a failing exit code.
Findings configured as FAIL still cause failure.
A successful scan does not mean the application has no findings.

### CI reports

Open the GitHub Actions workflow run and download the
zap-reports artifact. It contains zap-ci.html and zap-ci.json
when both reports were generated successfully.

Artifacts are configured to be retained for 7 days.
The upload step runs even after earlier failures, but it
cannot upload reports that were never generated.

### Stop the local application

Press Ctrl+C in the Flask terminal to stop the container.
The `--rm` option removes the container after it stops;
the image and network remain.

## Learning approach

Build one small component, verify its behaviour and explain the result
before adding the next component.

## Learning milestones

1. Local environment and Git: working directory, staging and commits.
2. GitHub: remotes, branches and pull requests.
3. A small local web application and basic automated tests.
4. Continuous Integration with GitHub Actions.
5. SAST: inspect a finding, fix it and scan again.
6. Docker and DAST against the local lab application.
7. Security gates, reports and project documentation.

## Limitations

- The application uses Flask's development server for this lab.
- ZAP Baseline performs crawling and passive scanning, not a
  full active security assessment.
- CSP and other reported warnings remain unresolved.
- Passing tests and scans do not prove the application is secure.
- The Docker images use mutable tags; future runs may use
  different image versions.

## Lab scope

Security testing is limited to this lab and explicitly authorised targets.
Use synthetic data and dummy credentials only.
My goal is to understand how security checks integrate into CI/CD.
I am practising changes on a Git branch.
