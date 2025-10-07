# reporter/cli.py
"""
Simple CLI wrapper:

Example:
python -m reporter.cli --findings findings.json --outdir out --html report.html --slack-webhook "$WEBHOOK" --smtp-host smtp.example.com --smtp-user user --smtp-pass $PASS --email to@example.com
"""
import argparse
import os
import json
from pathlib import Path
from reporter.reporter import Reporter

def load_findings(path: str):
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    # support either a list or {"findings": [...]} shape
    if isinstance(data, dict) and "findings" in data:
        return data["findings"], data.get("meta", {})
    if isinstance(data, list):
        return data, {}
    raise ValueError("Unsupported findings file format, must be list or object with key 'findings'.")

def main():
    p = argparse.ArgumentParser(description="Report generator CLI")
    p.add_argument("--findings", required=True, help="Path to findings JSON")
    p.add_argument("--outdir", default="out", help="Directory to write outputs")
    p.add_argument("--html", default="report.html", help="HTML output filename inside outdir")
    p.add_argument("--json", default="report.json", help="JSON output filename inside outdir")
    p.add_argument("--txt", default="report.txt", help="CLI/plaintext output filename inside outdir")
    p.add_argument("--templates", default=os.path.join(os.path.dirname(__file__), "templates"), help="Templates dir")
    p.add_argument("--slack-webhook", default=None, help="Slack incoming webhook URL")
    p.add_argument("--slack-max", type=int, default=6, help="Max findings in Slack message")
    p.add_argument("--smtp-host", default=None)
    p.add_argument("--smtp-port", type=int, default=587)
    p.add_argument("--smtp-user", default=None)
    p.add_argument("--smtp-pass", default=None)
    p.add_argument("--email-to", default=None, help="Comma separated list of recipients")
    p.add_argument("--no-html", action="store_true", help="Skip HTML generation")
    p.add_argument("--redact", action="store_true", help="Apply built-in redaction")
    args = p.parse_args()

    findings, meta = load_findings(args.findings)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    redact_fn = None
    if args.redact:
        from reporter.reporter import default_redact
        redact_fn = default_redact

    r = Reporter(findings=findings, repo=meta.get("repo") or meta.get("repository"), meta=meta, redact_fn=redact_fn)

    # JSON
    json_path = outdir / args.json
    r.write_json_file(str(json_path))

    # CLI text
    txt_path = outdir / args.txt
    r.write_cli_file(str(txt_path))

    # HTML
    if not args.no_html:
        html_path = outdir / args.html
        templates_dir = args.templates
        r.write_html_file(str(html_path), templates_dir=templates_dir)
        print(f"Wrote HTML report: {html_path}")

    print(f"Wrote JSON: {json_path}")
    print(f"Wrote text: {txt_path}")

    # Slack
    if args.slack_webhook:
        try:
            res = r.send_slack_webhook(args.slack_webhook, max_findings=args.slack_max)
            print("Slack send result:", res)
        except Exception as e:
            print("Slack send failed:", e)

    # Email
    if args.smtp_host and args.email_to:
        to_addrs = [x.strip() for x in args.email_to.split(",") if x.strip()]
        msg = r.email_message(to_addrs=to_addrs, templates_dir=(None if args.no_html else args.templates))
        try:
            r.send_email_smtp(args.smtp_host, args.smtp_port, args.smtp_user, args.smtp_pass, msg, use_starttls=True)
            print("Email sent")
        except Exception as e:
            print("Email send failed:", e)

if __name__ == "__main__":
    main()
