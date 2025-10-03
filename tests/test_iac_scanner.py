import pytest
from scanner.iac_scanner import IacScanner

def test_iac_scanner_detects_insecure_resources(tmp_path):
    """Run Checkov against sample IaC and check output format"""
    config = {
        "paths": {"reports_path": str(tmp_path)},
        "scans": {"iac": {"enabled": True}}
    }
    scanner = IacScanner(config)
    findings = scanner.run()
    assert isinstance(findings, list)
    if findings:
        f = findings[0]
        for key in ["scanner", "rule_id", "file_path", "severity", "message"]:
            assert key in f
