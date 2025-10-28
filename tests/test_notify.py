import json
from unittest.mock import patch
from scripts.notify import highest_severity, build_slack_message, send_slack

def test_highest_severity_detects_critical():
    """Ensure the notification logic detects highest severity correctly."""
    data = {
        "secrets": [{"severity": "LOW"}],
        "iac": [{"severity": "CRITICAL"}],
        "container": []
    }
    assert highest_severity(data) == "CRITICAL"

def test_build_slack_message_contains_total():
    """Slack message should include total findings and build ID."""
    data = {"secrets": [{}], "iac": [{}, {}], "container": []}
    msg = build_slack_message(data, build_id="b123")
    assert "Total findings" in msg
    assert "b123" in msg

@patch("scripts.notify.requests.post")
def test_send_slack_called(mock_post):
    """Verify Slack webhook is called."""
    send_slack("https://hooks.slack.com/test", "Test message")
    mock_post.assert_called_once()
