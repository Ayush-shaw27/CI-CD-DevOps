import json
def test_mock_report_loads():
    with open("reports/mock_report.json") as fh:
        data = json.load(fh)
    assert "secrets" in data
    assert "iac" in data
    assert "container" in data
