import pytest
from scanner.container_scanner import ContainerScanner

def test_container_scanner_runs(tmp_path):
    """Ensure container scanner runs and returns list"""
    config = {
        "paths": {"reports_path": str(tmp_path)},
        "scans": {"container": {"enabled": True}}
    }
    scanner = ContainerScanner(config)
    findings = scanner.run()
    assert isinstance(findings, list)

def test_container_findings_have_required_fields(tmp_path):
    """Check Trivy findings have consistent fields"""
    config = {"paths": {"reports_path": str(tmp_path)}}
    scanner = ContainerScanner(config)
    findings = scanner.run()
    if findings:
        f = findings[0]
        for key in ["scanner", "rule_id", "severity", "package", "message"]:
            assert key in f
