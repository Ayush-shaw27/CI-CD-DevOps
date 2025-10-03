import json

def test_mock_history_loads():
    with open("reports/mock_report_history.json") as fh:
        history = json.load(fh)

    assert isinstance(history, list)
    assert len(history) == 4
    for build in history:
        assert "build_id" in build
        assert "secrets" in build
        assert "iac" in build
        assert "container" in build
