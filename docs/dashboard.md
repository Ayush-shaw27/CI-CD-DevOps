# 🧠 CI/CD Security Dashboard Documentation

## 📌 Overview

The **CI/CD Security Dashboard** is a modern, responsive web interface that visualizes the results of automated security scans run during the CI/CD pipeline.  
It provides an at-a-glance view of the current security health of the project — helping developers, DevOps engineers, and security teams track vulnerabilities across **Secrets**, **IaC**, and **Container** scans.

---

## 🎯 Purpose

- Provide **real-time insights** into CI/CD scan results.
- Visualize vulnerabilities by **severity, category, and trend**.
- Enable **data-driven decision-making** for secure deployments.
- Serve as a single point of truth for the entire DevSecOps workflow.

---

## 🧩 Data Flow

1. **Pipeline Execution**
   - The GitHub Actions workflow runs on every push or pull request.
   - It triggers the **GitLeaks**, **Checkov**, and **Trivy** scanners.

2. **Report Generation**
   - Each scanner produces a JSON report under `reports/`.
   - These include:  
     - `reports/gitleaks-latest.json`  
     - `reports/checkov-latest.json`  
     - `reports/trivy-latest.json`

3. **Data Aggregation**
   - The plugin combines these outputs into a unified file:
     ```
     reports/mock_report.json
     ```
   - A history of past runs is maintained in:
     ```
     reports/mock_report_history.json
     ```

4. **Dashboard Rendering**
   - The frontend (React/Vite/Next.js) fetches the JSON files from the API or local storage.
   - Data is displayed as charts and tables, showing severity distribution and vulnerability trends.

---

## 🖥️ Dashboard Features

| Feature | Description |
|----------|--------------|
| **Vulnerability Overview** | Bar or pie chart showing CRITICAL, HIGH, MEDIUM, LOW counts |
| **Scan Summary Cards** | Separate cards for Secrets, IaC, and Containers |
| **Trend Over Time** | Line chart showing total vulnerabilities per build/run |
| **Detailed Findings Table** | Expandable rows with rule IDs, file paths, and messages |
| **Responsive Layout** | Mobile-friendly, built with modern UI components (Tailwind, Chart.js, or Recharts) |
| **Auto-refresh** | Optionally updates when new reports are generated or uploaded |

---

## ⚙️ Setup Instructions

### 1️⃣ Frontend Setup

If the dashboard is a separate frontend project:
```bash
cd dashboard/
npm install
npm run dev
```
Then open: `http://localhost:5173` or the configured local dev port.

If it's integrated into the FastAPI backend:
- The dashboard is served from `/dashboard` endpoint.
- Start the backend with: `python main.py`
- Then visit: `http://localhost:8000/dashboard`

### 2️⃣ Connecting Data

Make sure the dashboard reads reports from:
- `reports/mock_report.json`
- `reports/mock_report_history.json`

If deployed to AWS:
- Reports are uploaded to an S3 bucket (e.g., `s3://ci-cd-devops-reports/`)
- The dashboard fetches these reports via S3 public URL or FastAPI endpoint proxying S3 data

---

## 📊 Sample Data Structure

```json
{
  "secrets": [
    {"scanner": "GitLeaks", "rule_id": "AWS001", "file_path": "api/auth.py", "severity": "HIGH", "message": "Hardcoded AWS key"}
  ],
  "iac": [
    {"scanner": "Checkov", "rule_id": "CKV_AWS_20", "file_path": "terraform/main.tf", "severity": "CRITICAL", "message": "S3 bucket allows public read access"}
  ],
  "container": [
    {"scanner": "Trivy", "rule_id": "TRV001", "file_path": "Dockerfile", "severity": "MEDIUM", "message": "Outdated OpenSSL version"}
  ]
}
```

---

## 🧮 Key Metrics Displayed

| Metric | Description |
|--------|-------------|
| **Total Vulnerabilities** | Combined count from all scanners |
| **By Severity** | Breakdown (CRITICAL, HIGH, MEDIUM, LOW) |
| **By Category** | Secrets vs IaC vs Container |
| **Build Comparison** | Vulnerability change trend across runs |
| **Policy Compliance** | Pass/fail indicator based on severity thresholds |

---

## 🚀 Deployment

When CI/CD runs successfully:
1. The GitHub Actions workflow pushes reports to AWS S3
2. The backend or frontend dashboard auto-updates to reflect new data
3. The dashboard is accessible from your deployed Medical Records Site

Ensure:
- The deployment user has AWS credentials configured in GitHub Secrets
- S3 CORS permissions allow public read or proxy access

---

## 🧰 Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| **Dashboard not loading data** | JSON path incorrect or file missing | Verify reports exist and are valid JSON |
| **Charts empty or NaN values** | Malformed report data | Regenerate reports with valid output |
| **CORS errors when fetching from S3** | CORS policy misconfigured | Update S3 bucket CORS policy |
| **Dashboard not updating** | Cached data | Clear browser cache or re-run pipeline |

---

## ✅ Verification Checklist

- [ ] Dashboard loads without errors
- [ ] Displays correct severity distribution
- [ ] Fetches and parses latest reports automatically
- [ ] Responsive on mobile + desktop
- [ ] Deployed link works on production site

---

## 🏁 Summary

The CI/CD Security Dashboard closes the feedback loop between security scanning and deployment. By visualizing real-time DevSecOps metrics, it enables proactive vulnerability management and ensures every deployment is verified, secure, and compliant.

**Author:** QA & Documentation Engineer  
**Phase:** 4 (Integration & Visualization)  
**Last Updated:** *15th October 2025*
