# 🔔 Alerts & Notifications Setup Guide

## Overview
The notification module sends alerts after CI/CD security scans complete.

**Supported channels:**
- **Slack** (via webhook)
- **Email** (via SMTP)

---

## 🧭 1. Slack Setup

### Steps:
1. In Slack, go to **Apps → Custom Integrations → Incoming Webhooks**
2. Create a webhook → select channel → copy the generated URL
3. In your GitHub repository → **Settings → Secrets and variables → Actions → New repository secret**
   - **Name:** `SLACK_WEBHOOK_URL`
   - **Value:** *(paste your Slack webhook URL)*

4. Verify Slack notifications are enabled in your config file (`config/config.yaml`):

```yaml
notifications:
  slack:
    enabled: true
    fail_on: ["CRITICAL", "HIGH"]
    webhook_env_var: "SLACK_WEBHOOK_URL"
```

---

## 📧 2. Email Setup (Optional)

### GitHub Secrets Configuration:
Add the following secrets in GitHub if email notifications are required:

- `SMTP_USER`
- `SMTP_PASS`

### Configuration in `config/config.yaml`:

```yaml
notifications:
  email:
    enabled: true
    fail_on: ["CRITICAL"]
    smtp:
      host: "smtp.gmail.com"
      port: 587
      user_env_var: "SMTP_USER"
      pass_env_var: "SMTP_PASS"
    recipients:
      - "team@example.com"
```

---

## 🧪 3. Local Testing

### Steps:
1. Activate your environment and run:

```powershell
.\.venv\Scripts\Activate.ps1
python scripts/notify.py
```

### Expected Results:
- Message appears in your Slack channel
- (Optional) Email sent to the configured address

---

## ⚙️ 4. GitHub Actions Integration

```yaml
- name: Notify on Failure
  if: failure()
  run: python scripts/notify.py
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
    SMTP_USER: ${{ secrets.SMTP_USER }}
    SMTP_PASS: ${{ secrets.SMTP_PASS }}
```

---

## 🚑 5. Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `requests.exceptions.ConnectionError` | Invalid Slack URL | Re-create webhook |
| `SMTPAuthenticationError` | Bad credentials | Update GitHub secrets |
| No alerts triggered | No CRITICAL/HIGH findings | Lower thresholds in config |
| `yaml.YAMLError` | Broken YAML format | Validate indentation |

---

**Validated By:** QA Team  
**Last Updated:** Phase 5 (Alerts & Notifications)
