import os
import json
import pytest
from scanner.gitleaks_scanner import GitLeaksScanner

def test_secret_scanner_runs(tmp_path):
    """Ensure GitLeaks scanner runs and returns findings list"""
    config = {
        "paths": {"reports_path": str(tmp_path)},
        "scans": {"secrets": {"enabled": True}}
    }
    scanner = GitLeaksScanner(config)
    findings = scanner.run()
    assert isinstance(findings, list)

def test_secret_scanner_output_format(tmp_path):
    """Check that each finding has required fields"""
    config = {"paths": {"reports_path": str(tmp_path)}}
    scanner = GitLeaksScanner(config)
    findings = scanner.run()
    if findings:  # only check if something found
        f = findings[0]
        for key in ["scanner", "rule_id", "file_path", "severity", "message"]:
            assert key in f
