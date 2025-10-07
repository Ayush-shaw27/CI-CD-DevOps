# scripts/generate_report.py
import os
import json
from reporter.reporter import Reporter

sample_findings = [
    {"title":"Hardcoded AWS key", "description":"Found AWS_ACCESS_KEY_ID in config.yml", "severity":"HIGH", "file":"config.yml", "line":12, "policy":"gitleaks-aws-key"},
    {"title":"Open S3 bucket", "description":"S3 had public read", "severity":"CRITICAL", "file":"terraform/s3.tf", "line":5, "policy":"checkov-aws-1"},
    {"title":"Outdated base image", "description":"Base image has CVE-2024-xxxx", "severity":"MEDIUM", "file":"Dockerfile", "policy":"trivy-image"},
]

r = Reporter(findings=sample_findings, repo="github.com/org/repo", meta={"report_url":"https://ci.example.com/reports/1234"}, redact_fn=None)
out_dir = "out"
os.makedirs(out_dir, exist_ok=True)
r.write_json_file(os.path.join(out_dir, "report.json"))
r.write_cli_file(os.path.join(out_dir, "report.txt"))
templates_dir = os.path.join(os.path.dirname(__file__), "..", "reporter", "templates")
r.write_html_file(os.path.join(out_dir, "report.html"), templates_dir=templates_dir)
print("Wrote out/report.{json,txt,html}")
