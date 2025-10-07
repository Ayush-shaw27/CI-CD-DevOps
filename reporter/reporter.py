# reporter/reporter.py
"""
Reporter module
- Build normalized findings
- Output JSON, CLI, HTML (Jinja2)
- Build Slack payload and send via webhook
- Build EmailMessage and send via SMTP
- Redaction helpers for secrets / PHI
"""

from __future__ import annotations
import json
import datetime
import smtplib
from email.message import EmailMessage
from typing import List, Dict, Optional, Any, Callable
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import textwrap
import re

try:
    import requests
except Exception:
    requests = None  # Slack sending will check

# Severity ordering & colors
SEVERITY_ORDER = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]
SEVERITY_COLORS = {
    "CRITICAL": "#d32f2f",
    "HIGH": "#f57c00",
    "MEDIUM": "#fbc02d",
    "LOW": "#1976d2",
    "INFO": "#455a64",
}

def normalize_severity(s: str) -> str:
    if not s:
        return "INFO"
    s = s.strip().upper()
    return s if s in SEVERITY_ORDER else "INFO"

def default_redact(text: str, patterns: Optional[List[str]] = None) -> str:
    """
    Very conservative redaction:
    - If 'patterns' provided (regex strings), replace matches with '[REDACTED]'
    - Also redact anything that looks like an AWS key, long hex, JWT-looking token (best-effort)
    """
    if text is None:
        return text
    out = text
    # basic patterns
    default_patterns = [
        r"AKIA[0-9A-Z]{16}",              # AWS-ish
        r"(?i)aws_secret_access_key.?[:=]\s*[A-Za-z0-9/+=]{16,}",  # key:value
        r"(?:eyJ[a-zA-Z0-9_\-]+?\.[a-zA-Z0-9_\-]+?\.[a-zA-Z0-9_\-]+)",  # JWT
        r"[A-Fa-f0-9]{32,}",             # long hex (CAVEAT: could redact hashes)
        r"\b(?:\d[ -]*?){13,16}\b",      # credit-card-ish
        r"\b\d{3}-\d{2}-\d{4}\b",        # SSN US
        r"\b(?:\d{10,12})\b",            # phone-ish
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"  # emails
    ]
    use_patterns = (patterns or []) + default_patterns
    for p in use_patterns:
        try:
            out = re.sub(p, "[REDACTED]", out)
        except re.error:
            # ignore bad pattern
            continue
    return out

class Reporter:
    def __init__(
        self,
        findings: List[Dict[str, Any]],
        scan_id: Optional[str] = None,
        repo: Optional[str] = None,
        timestamp: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None,
        redact_fn: Optional[Callable[[str], str]] = None
    ):
        """
        findings: list of dicts (title, description, severity, file, line, policy, extra...)
        redact_fn: function that accepts a string and returns redacted string
        """
        self.redact_fn = redact_fn or (lambda s: default_redact(s) if isinstance(s, str) else s)
        self.findings = [self._normalize_f(f) for f in findings]
        self.scan_id = scan_id or f"scan-{datetime.datetime.utcnow().isoformat()}"
        self.repo = repo
        self.timestamp = timestamp or datetime.datetime.utcnow().isoformat() + "Z"
        self.meta = meta or {}

    def _normalize_f(self, f: Dict[str, Any]) -> Dict[str, Any]:
        f = dict(f)
        f["severity"] = normalize_severity(f.get("severity", "INFO"))
        f.setdefault("id", f.get("id") or (f.get("title")[:48] if f.get("title") else f"finding-{len(f)}"))
        f.setdefault("file", f.get("file") or "")
        f.setdefault("line", f.get("line") or "")
        f.setdefault("policy", f.get("policy") or "")
        # redact text fields
        for k in ("title", "description", "file", "policy"):
            if k in f and isinstance(f[k], str):
                f[k] = self.redact_fn(f[k])
        return f

    # JSON output
    def to_json(self, pretty: bool = True) -> str:
        payload = {
            "scan_id": self.scan_id,
            "repo": self.repo,
            "timestamp": self.timestamp,
            "summary": self.summary_dict(),
            "findings": self.findings,
            "meta": self.meta,
        }
        return json.dumps(payload, indent=2 if pretty else None, sort_keys=False)

    def write_json_file(self, out_path: str):
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(self.to_json(pretty=True))

    # CLI/plain text output
    def summary_dict(self) -> Dict[str, int]:
        counts = {k: 0 for k in SEVERITY_ORDER}
        for f in self.findings:
            counts[f["severity"]] = counts.get(f["severity"], 0) + 1
        counts["TOTAL"] = len(self.findings)
        return counts

    def to_cli(self) -> str:
        s = []
        s.append(f"Scan ID: {self.scan_id}")
        if self.repo:
            s.append(f"Repo: {self.repo}")
        s.append(f"Timestamp: {self.timestamp}")
        s.append("")
        s.append("Summary:")
        sd = self.summary_dict()
        for sev in SEVERITY_ORDER:
            s.append(f"  {sev:8} : {sd.get(sev,0)}")
        s.append(f"  TOTAL   : {sd['TOTAL']}")
        s.append("")
        if not self.findings:
            s.append("No findings.")
            return "\n".join(s)

        s.append("Findings:")
        for i, f in enumerate(sorted(self.findings, key=lambda x: SEVERITY_ORDER.index(x["severity"]))):
            header = f"[{f['severity']}] {f.get('title')}"
            s.append(header)
            loc = f"{f.get('file') or '<unknown>'}"
            if f.get("line"):
                loc += f":{f['line']}"
            s.append(f"  Location : {loc}")
            if f.get("policy"):
                s.append(f"  Policy   : {f.get('policy')}")
            desc = textwrap.indent(textwrap.fill(f.get("description","").strip(), width=78), "  ")
            s.append(f"  Description:")
            s.append(desc)
            s.append("-" * 72)
        return "\n".join(s)

    def write_cli_file(self, out_path: str):
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(self.to_cli())

    # HTML output via Jinja2
    def to_html(self, templates_dir: str, template_name: str = "report.html.j2", context_extra: Optional[Dict] = None) -> str:
        env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )
        template = env.get_template(template_name)
        context = {
            "scan_id": self.scan_id,
            "repo": self.repo,
            "timestamp": self.timestamp,
            "meta": self.meta,
            "findings": sorted(self.findings, key=lambda x: (SEVERITY_ORDER.index(x["severity"]), x.get("file"))),
            "severity_colors": SEVERITY_COLORS,
            "summary": self.summary_dict(),
        }
        if context_extra:
            context.update(context_extra)
        return template.render(**context)

    def write_html_file(self, out_path: str, templates_dir: str, template_name: str = "report.html.j2"):
        html = self.to_html(templates_dir=templates_dir, template_name=template_name)
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(html)

    # Slack payload builder (Block Kit)
    def slack_payload(self, max_findings: int = 6) -> Dict[str, Any]:
        summary = self.summary_dict()
        top = sorted(self.findings, key=lambda x: SEVERITY_ORDER.index(x["severity"]))[:max_findings]
        blocks = []
        header_text = f"*Security scan result* — repo: `{self.repo or 'unknown'}` — `{self.scan_id}`"
        blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": header_text}})
        blocks.append({"type": "context", "elements": [{"type": "mrkdwn", "text": f"*Summary:* CRITICAL {summary['CRITICAL']}  •  HIGH {summary['HIGH']}  •  MEDIUM {summary['MEDIUM']}  •  LOW {summary['LOW']}  •  INFO {summary['INFO']}"}]})
        blocks.append({"type": "divider"})

        if not top:
            blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": "_No findings_ 🎉"}})
        else:
            for f in top:
                sev = f["severity"]
                title = f"*[{sev}]* {f.get('title')}"
                loc = f"{f.get('file') or '—'}"
                if f.get('line'):
                    loc += f":{f['line']}"
                desc = (f.get("description") or "")[:600]
                text = f"{title}\n`{loc}`\n{desc}"
                blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": text}})
                blocks.append({"type": "divider"})

        if self.meta.get("report_url"):
            blocks.append({
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "View full report"},
                        "url": self.meta["report_url"]
                    }
                ]
            })

        payload = {
            "blocks": blocks,
            "text": f"Scan results for {self.repo or 'repo'} — {self.scan_id}"
        }
        return payload

    def send_slack_webhook(self, webhook_url: str, max_findings: int = 6, timeout: int = 10) -> Dict[str, Any]:
        """
        Post to Slack incoming webhook. Requires 'requests' installed.
        Returns requests.Response.json() or raises RuntimeError if requests not present.
        """
        if requests is None:
            raise RuntimeError("requests not installed; cannot send to Slack.")
        payload = self.slack_payload(max_findings=max_findings)
        headers = {"Content-Type": "application/json"}
        r = requests.post(webhook_url, json=payload, headers=headers, timeout=timeout)
        r.raise_for_status()
        # Slack webhook usually returns text "ok"
        try:
            return {"status": "ok", "text": r.text, "code": r.status_code}
        except Exception:
            return {"status": "ok", "code": r.status_code}

    # Email helpers
    def email_message(self, subject: Optional[str] = None, to_addrs: Optional[List[str]] = None, from_addr: Optional[str] = None, templates_dir: Optional[str] = None) -> EmailMessage:
        subject = subject or f"[Scan] {self.repo or 'repo'} — {self.summary_dict().get('TOTAL',0)} findings"
        to_addrs = to_addrs or []
        from_addr = from_addr or "scanner@example.com"
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = from_addr
        msg["To"] = ", ".join(to_addrs)
        plain = self.to_cli()
        msg.set_content(plain)

        if templates_dir:
            html = self.to_html(templates_dir=templates_dir)
            msg.add_alternative(html, subtype="html")
        else:
            html = "<html><body><pre>{}</pre></body></html>".format(plain.replace("<","&lt;"))
            msg.add_alternative(html, subtype="html")
        return msg

    def send_email_smtp(self, smtp_host: str, smtp_port: int, username: Optional[str], password: Optional[str], msg: EmailMessage, use_starttls: bool = True, timeout: int = 30):
        """
        Sends EmailMessage via SMTP.
        If use_starttls True -> SMTP + starttls
        Otherwise -> SMTP_SSL
        """
        if use_starttls:
            server = smtplib.SMTP(smtp_host, smtp_port, timeout=timeout)
            server.ehlo()
            server.starttls()
            server.ehlo()
        else:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=timeout)
        try:
            if username and password:
                server.login(username, password)
            server.send_message(msg)
        finally:
            try:
                server.quit()
            except Exception:
                pass

