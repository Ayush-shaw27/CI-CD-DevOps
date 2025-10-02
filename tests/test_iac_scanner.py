import os
from ci_cd_plugin.scanners.iac_scanner import IacScanner
from ruamel.yaml import YAML

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml"))

def load_config():
    yaml = YAML(typ="safe")
    with open(CONFIG_PATH, "r", encoding="utf-8") as fh:
        return yaml.load(fh)

def test_iac_scanner_detects_insecure_resources(tmp_path):
    config = load_config()
    config["paths"]["reports_path"] = str(tmp_path)
    scanner = IacScanner(config)
    findings = scanner.run()
    assert isinstance(findings, list)
    assert len(findings) > 0
    f = findings[0]
    for k in ["scanner", "rule_id", "file_path", "severity", "message"]:
        assert k in f
    assert f["severity"].upper() in ("CRITICAL","HIGH","MEDIUM","LOW","UNKNOWN")
