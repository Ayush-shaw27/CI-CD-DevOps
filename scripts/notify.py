"""
notify.py — CI/CD Alerts and Notifications Module
-------------------------------------------------
Sends alerts via Slack (and optionally Email) when scans detect critical vulnerabilities.
Triggered automatically from CI workflows or run manually.
"""

import os
import json
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

REPORT_PATH = Path("reports/mock_report.json")  # Update to latest report path if needed

def load_report():
    """Load JSON report from reports folder."""
    if not REPORT_PATH.exists():
        print(f"[!] Report not found at {REPORT_PATH}")
        return {}
    with open(REPORT_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)

def highest_severity(report):
    """Return the highest severity level found."""
    levels = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1, "UNKNOWN": 0}
    max_level = 0
    for cat in ["secrets", "iac", "container"]:
        for item in report.get(cat, []):
            sev = item.get("severity", "UNKNOWN").upper()
            max_level = max(max_level, levels.get(sev, 0))
    for name, val in levels.items():
        if val == max_level:
            return name
    return "UNKNOWN"

def build_slack_message(report, build_id="local"):
    """Format message for Slack notification."""
    total = sum(len(report.get(k, [])) for k in ["secrets", "iac", "container"])
    sev = highest_severity(report)
    msg = f"""
*🔒 CI/CD Security Alert*
Build ID: `{build_id}`

*Highest Severity:* {sev}
*Total Findings:* {total}

See full report in `reports/mock_report.json`
    """
    return msg.strip()

def send_slack(webhook_url, message):
    """Send message to Slack via webhook."""
    try:
        requests.post(webhook_url, json={"text": message}, timeout=5)
        print("[+] Slack alert sent successfully.")
    except Exception as e:
        print(f"[!] Slack notification failed: {e}")

def send_email(report):
    """Optional: Send summary email alert."""
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    recipients = os.getenv("ALERT_RECIPIENTS", "").split(",")

    if not smtp_user or not smtp_pass or not recipients:
        print("[!] Email credentials or recipients not configured.")
        return

    sev = highest_severity(report)
    body = f"Security scan completed.\nHighest severity: {sev}\nCheck reports folder for details."
    msg = MIMEMultipart()
    msg["Subject"] = f"[CI/CD Alert] Highest Severity: {sev}"
    msg["From"] = smtp_user
    msg["To"] = ", ".join(recipients)
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        print("[+] Email alert sent successfully.")
    except Exception as e:
        print(f"[!] Email send failed: {e}")

def main():
    """Main entry point for notifications."""
    report = load_report()
    if not report:
        print("[!] No report found or empty report.")
        return

    slack_url = os.getenv("SLACK_WEBHOOK_URL")
    if slack_url:
        msg = build_slack_message(report)
        send_slack(slack_url, msg)
    else:
        print("[!] Slack webhook not configured.")

    # Optional email
    send_email(report)

if __name__ == "__main__":
    main()
