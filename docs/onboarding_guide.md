# 🧭 Developer Onboarding Guide

## 📘 Project Overview

Welcome to the **Medical Records API – DevSecOps Backend** project.

This system combines:

- A **FastAPI-based backend** for secure medical data management
- A **DevSecOps CI/CD pipeline** with automated security scans
- A **Responsive Security Dashboard** visualizing vulnerabilities and build trends

The goal is to demonstrate **end-to-end secure software delivery** in a realistic healthcare environment.

---

## ⚙️ Development Environment Setup

### 1️⃣ Prerequisites

Make sure you have the following installed on your system:

- **Python 3.11+**
- **MySQL 8+**
- **Git** (latest)
- **VS Code**
- **AWS Account** (optional for deployment phase)
- *(Optional for local scans)* GitLeaks, Checkov, Trivy

---

### 2️⃣ Clone the Repository

```bash
git clone https://github.com/Ayush-shaw27/CI-CD-DevOps.git
cd CI-CD-DevOps
```

---

### 3️⃣ Create a Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

---

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 5️⃣ Configure Environment Variables

Copy `.env.example` → `.env` and update credentials:

```
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/medical_records
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

```

---

### 6️⃣ Set Up Database

Launch MySQL shell:

```bash
mysql -u root -p
CREATE DATABASE medical_records;
CREATE DATABASE medical_records_test;
EXIT;

```

Seed initial data:

```bash
python database/seed_data.py

```

---

### 7️⃣ Verify Installation

Run server:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

```

Then visit:

- API Docs → http://localhost:8000/docs
- Dashboard → http://localhost:8000/dashboard

---

## 🔒 Security Scanning (DevSecOps Plugin)

### Run Local Scans

Run the integrated plugin manually:

```bash
python scripts/run_security_scan.py

```

Reports will be created in:

```
reports/gitleaks-latest.json
reports/gitleaks-history.json

```

---

### Run Tests (QA Validation)

Run all automated tests:

```bash
pytest -q

```

✅ Tests cover:

- API endpoints
- Database connection
- Scanners (GitLeaks, Checkov, Trivy)
- Config + Orchestration

---

## 🚀 CI/CD Pipeline (GitHub Actions)

### Overview

The project includes a **GitHub Actions** pipeline to automate:

1. Unit testing
2. Security scanning
3. Report upload to AWS S3
4. Auto-deployment to EC2

Workflow file:

`.github/workflows/ci_cd_pipeline.yml`

---

### Setup Secrets in GitHub

Go to your repository →

**Settings → Secrets and Variables → Actions**

Add these secrets:

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
EC2_IP

```

---

### AWS Configuration (for CI/CD Specialist)

- **S3 Bucket:** `devsecops-scan-reports`
- **EC2 Instance:** Host FastAPI backend
- **IAM Policies:** AmazonS3FullAccess, AmazonEC2FullAccess

---

## 🧠 Understanding the Project Architecture

### 📁 Modules

| Component | Function |
| --- | --- |
| **API** | FastAPI routes for authentication, patient CRUD |
| **Scanner** | Python wrapper to execute GitLeaks, Checkov, Trivy |
| **Scripts** | CLI automation for scans |
| **Dashboard** | Web UI visualizing scan trends |
| **Docs** | Developer and setup guides |
| **Tests** | Unit + integration tests for QA |
| **CI/CD** | Automated pipeline using GitHub Actions and AWS |

---

## 💻 Frontend Security Dashboard

### Live Path:

```
http://<your-ec2-ip>/dashboard

```

### Tech Stack:

- HTML5 + Bootstrap 5
- Chart.js (visualization)
- JS Fetch API (loads JSON data from /reports or S3)

### Data Source:

`reports/mock_report_history.json` (or real CI/CD-generated report)

Dashboard automatically updates when new scans are uploaded.

---

## 🧾 Team Roles & Responsibilities

| Role | Responsibilities |
| --- | --- |
| **Backend Developer** | Core API logic, config orchestration |
| **Frontend Developer** | Dashboard design & Chart.js integration |
| **CI/CD Specialist** | GitHub Actions + AWS pipeline |
| **DevSecOps Engineer** | Configure scanners, verify vulnerabilities |
| **Reporting & Notifications Engineer** | Generate HTML/Slack reports |
| **QA & Documentation Engineer** | Write docs, tests, and verification checklist |

---

## 🧩 Common Issues & Fixes

| Problem | Solution |
| --- | --- |
| `ModuleNotFoundError` | Activate venv → `venv\Scripts\activate` |
| `checkov/gitleaks not found` | Install via `pip install checkov gitleaks` |
| `Database not connecting` | Verify `.env` and DB name, ensure MySQL is running |
| `AWS upload failed` | Verify IAM permissions and region |
| `Dashboard blank` | Check `/reports/mock_report_history.json` path |

---

## ✅ Final Verification Checklist

1. App runs locally
2. Tests pass (`pytest`)
3. Security scans generate valid reports
4. GitHub Actions pipeline runs successfully
5. Reports visible on dashboard (local or AWS)
6. Documentation up-to-date (`docs/` + `README.md`)

---

## 📜 Summary

You are now fully onboarded!

You can:

- Run the backend API locally
- Execute DevSecOps scans
- View live vulnerability dashboards
- Deploy and verify through GitHub Actions + AWS

Your work ensures that **the Medical Records App remains secure, automated, and industry-compliant** — reflecting real-world healthcare DevSecOps practices.
