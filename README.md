# 🏥 Medical Records API — DevSecOps Integrated CI/CD Project

A **secure medical records management system** built using **FastAPI**, **SQLAlchemy**, and **JWT authentication**, integrated with a **DevSecOps CI/CD plugin** that performs **automated security scans** (GitLeaks, Checkov, Trivy), **report generation**, and **Slack/email alerts**.

---

## 🚀 Project Structure

```
CI-CD-DevOps/
├── api/                    # FastAPI endpoints
├── auth/                   # JWT & password utilities
├── database/               # SQLAlchemy models & seed data
├── scanner/                # Security scanners integration
├── scripts/
│   ├── run_security_scan.py # Executes security scans
│   └── notify.py           # Slack/Email notification logic
├── tests/                  # Unit tests for API, scanners, and alerts
├── reports/                # Scan output (mock_report.json, etc.)
├── docs/                   # Documentation (setup, verify, notify)
├── main.py                 # FastAPI entrypoint
├── config/                 # YAML configuration for scanners
├── requirements.txt
└── .github/workflows/      # CI/CD workflows (GitHub Actions)
```

---

## ⚙️ Requirements

- **Python 3.10+**
- **MySQL 8.x** (or compatible)
- **Git**
- **Virtual Environment**
- **Optional:** Docker, GitLeaks, Checkov, Trivy (for full scans)

---

## 🧩 Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Ayush-shaw27/CI-CD-DevOps.git
cd CI-CD-DevOps
```

### 2️⃣ Create and Activate Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment

Copy `.env.example` → `.env` and update:

```ini
DATABASE_URL=mysql+pymysql://user:pass@localhost:3306/medical_records
SECRET_KEY=your-secret
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🧠 Running the API

```bash
uvicorn main:app --reload
```

- **API Docs:** http://localhost:8000/docs
- **Redoc:** http://localhost:8000/redoc

---

## 🔒 DevSecOps Integration Overview

### ✅ Automated Scans

Security checks run via:

- **GitLeaks** — Secrets detection
- **Checkov** — Infrastructure-as-Code scan
- **Trivy** — Container image vulnerability scan

Triggered automatically in CI/CD pipeline or manually:

```bash
python scripts/run_security_scan.py
```

**Reports generated under `/reports/`:**
- `mock_report.json` — latest scan
- `mock_report_history.json` — previous builds

---

## 📊 CI/CD Security Dashboard

Built by the frontend developer using React/Vue.

- Displays scan history, severity counts, and trends
- Pulls data from `/reports/mock_report_history.json`

---

## 🔔 Alerts & Notifications

### Slack Alerts
- Configured via GitHub Secrets → `SLACK_WEBHOOK_URL`
- Triggered automatically in CI on failed build:

```bash
python scripts/notify.py
```

### Email Alerts (Optional)
Add secrets:
- `SMTP_USER`
- `SMTP_PASS`
- `ALERT_RECIPIENTS` (comma-separated)

Script automatically emails on CRITICAL or HIGH findings.

*See `docs/notify.md` for setup guide.*

---

## 🧪 Testing

Run all tests (including notification tests):

```bash
pytest -q
```

**Tests are located in `/tests/`:**
- `test_api.py` — FastAPI endpoints
- `test_iac_scanner.py` — IaC scanner logic
- `test_secret_scanner.py` — GitLeaks wrapper
- `test_notify.py` — Notification module tests

---

## 🧭 QA Verification Checklist

*See `docs/verification_checklist.md`*

- [ ] Run all unit tests
- [ ] Validate Slack alerts
- [ ] Verify reports format
- [ ] Confirm configuration matches `config/config.yaml`

---

## 🧰 GitHub Actions CI/CD Pipeline

**Workflow:** `.github/workflows/local_ci.yml`

- Runs `pytest`
- Executes `run_security_scan.py`
- Uploads reports as artifacts
- Sends Slack alerts on failure

---

## 🩺 Project Summary

| Role | Responsibilities |
|------|------------------|
| Backend Developer | Core logic, plugin orchestration, policy engine |
| DevSecOps Engineer | Integrates GitLeaks, Checkov, Trivy |
| QA Engineer | Unit tests, docs, verification |
| CI/CD Specialist | GitHub Actions setup, artifact upload |
| Frontend Developer | Builds security dashboard visualization |

---

## 🧾 License

This project is for educational and demonstration purposes only.  
All trademarks and libraries belong to their respective owners.
