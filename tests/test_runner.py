import pytest
from core.runner import PluginRunner

def test_runner_loads_config(tmp_path):
    """Runner should load config and initialize scanners"""
    config = {
        "paths": {"reports_path": str(tmp_path)},
        "scans": {
            "secrets": {"enabled": True},
            "iac": {"enabled": True},
            "container": {"enabled": False},
        }
    }
    runner = PluginRunner(config)
    assert hasattr(runner, "scanners")
    assert isinstance(runner.scanners, list)

def test_runner_executes_all_enabled_scanners(tmp_path):
    """Runner should collect results from all enabled scanners"""
    config = {
        "paths": {"reports_path": str(tmp_path)},
        "scans": {
            "secrets": {"enabled": True},
            "iac": {"enabled": True},
        }
    }
    runner = PluginRunner(config)
    all_findings = runner.run()
    assert isinstance(all_findings, dict)
    assert "secrets" in all_findings
    assert "iac" in all_findings

def test_runner_exit_codes(tmp_path):
    """Policy engine should return correct exit code"""
    config = {
        "paths": {"reports_path": str(tmp_path)},
        "scans": {"iac": {"enabled": True}},
        "policy": {"fail_on": ["CRITICAL"], "warn_on": ["HIGH", "MEDIUM"]}
    }
    runner = PluginRunner(config)
    exit_code = runner.execute_pipeline()
    assert exit_code in (0, 2)
