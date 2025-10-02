#!/usr/bin/env python3
import json, sys
from pathlib import Path

def main(report_path):
    p = Path(report_path)
    if not p.exists():
        print(f"No report found at {report_path}")
        sys.exit(1)

    data = json.loads(p.read_text(encoding='utf-8'))
    findings = data if isinstance(data, list) else data.get("results", [])
    count = len(findings)
    print(f"gitleaks findings count: {count}")

    for f in findings[:20]:
        path = f.get("file", f.get("Path", "unknown"))
        rule = f.get("rule", f.get("Rule", "unknown"))
        commit = f.get("commit", f.get("Commit", "N/A"))
        print(f"- {path} rule={rule} commit={commit}")

    if count > 0:
        print("SECRET FINDINGS DETECTED. Failing job to block merge.")
        sys.exit(2)

    print("No secrets found. Passing.")
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: parse_gitleaks.py <report.json>")
        sys.exit(1)
    main(sys.argv[1])
