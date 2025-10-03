# CI/CD Security Plugin - DevSecOps Project

A modular, security-focused plugin that integrates into CI/CD pipelines (GitHub Actions, Jenkins) to automatically scan for:
- **Secrets** in code (using GitLeaks)
- **Infrastructure-as-Code (IaC) misconfigurations** (using Checkov)
- **Container vulnerabilities** (using Trivy)

The plugin ensures security checks are automated before deployment, preventing leaks, misconfigurations, and vulnerabilities from reaching production.

---

## 📌 Project Overview
This project demonstrates a **CI/CD Security Plugin** integrated into a real-world **E-Commerce Site pipeline**. The plugin acts as a *security stage* inside CI/CD, enforcing "shift-left security" by catching issues early in development.

**Example Workflow:**
1. Developer pushes code to GitHub.
2. GitHub Actions pipeline starts:
   - Build → Test → **Security Scan (Plugin)** → Deploy.
3. The plugin scans for secrets, IaC misconfigs, and container vulnerabilities.
4. Reports are generated and build passes/fails based on policy thresholds.

---

## 🏗 Architecture

```
ci-cd-security-plugin/
├── config/               # YAML/JSON config files (scan settings, thresholds)
│   └── config.yaml
├── src/
│   └── ci_cd_plugin/
│       ├── scanners/     # SecretScanner, IacScanner, ContainerScanner
│       ├── core/         # Orchestrator to run scanners
│       ├── policy/       # Policy Engine (fail/pass logic)
│       └── reporter/     # Report generator (JSON/CLI/HTML)
├── infra/                # Example Terraform/CloudFormation files
├── tests/                # Unit tests
├── reports/              # Generated reports
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## ⚙️ Config (config/config.yaml)

```yaml
project:
  name: "secscan-demo"
  version: "0.1.0"

paths:
  repo_root: "."
  iac_path: "infra"
  reports_path: "reports"

scans:
  secrets:
    enabled: true
    tool: "gitleaks"
  iac:
    enabled: true
    tool: "checkov"
    severity_thresholds:
      fail_on: ["HIGH", "CRITICAL"]
      warn_on: ["MEDIUM"]
  container:
    enabled: true
    tool: "trivy"

report:
  formats: ["json", "cli"]
  redact_values: true
  save_raw_tool_outputs: true
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- Git
- Docker Desktop (for Trivy)
- GitHub account

### Installation
```bash
# Clone the repo
git clone <your-repo-url>
cd ci-cd-security-plugin

# Setup virtual environment
python -m venv .venv
source .venv/bin/activate   # (Linux/macOS)
.\.venv\Scriptsctivate    # (Windows PowerShell)

# Install dependencies
pip install -r requirements.txt
```

---

## 🔍 Running the Plugin

### Run Locally
```bash
python -m src.ci_cd_plugin.core.run --config config/config.yaml
```

### Run Secret Scanner Only
```bash
gitleaks detect --source . --report-format json --report-path reports/gitleaks.json
```

### Run IaC Scanner Only
```bash
checkov -d infra -o json > reports/checkov.json
```

### Run Container Scanner Only
```bash
trivy fs . --format json --output reports/trivy.json
```

---

## 📊 Reports & Frontend

The plugin generates:
- **CLI Output** → Build logs in GitHub Actions.
- **JSON Reports** → For automation & machine processing.
- **HTML Reports** (optional) → Human-readable summary with severity breakdowns.

Reports show:
- Number of issues found
- Severity breakdown (Critical, High, Medium, Low)
- Files/lines/resources affected
- Pass/Fail decision

---

## 🔗 CI/CD Integration (GitHub Actions Example)

Create `.github/workflows/security-scan.yml`:

```yaml
name: Security Scan

on:
  push:
    branches: [ "main" ]
  pull_request:

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run Security Plugin
        run: python -m src.ci_cd_plugin.core.run --config config/config.yaml

      - name: Upload Reports
        uses: actions/upload-artifact@v3
        with:
          name: security-reports
          path: reports/
```

---

## 🏥 Example Use Case (E-Commerce Site)

The plugin is demonstrated on an **E-Commerce pipeline** because:
- Handles **payments & user accounts** → needs strict security.
- Has **backend code, IaC, and containers** → all three scanner types apply.
- Industry relevance → PCI-DSS & cloud compliance.

---

## 📈 Future Enhancements

- Parallel scanning for faster runs
- Slack/Email notifications for critical findings
- Scheduled scans (nightly/weekly)
- Central dashboard with visualizations
- Extend support for Azure & GCP IaC scanning

---

## 📜 License
This project is licensed under the MIT License.

---
