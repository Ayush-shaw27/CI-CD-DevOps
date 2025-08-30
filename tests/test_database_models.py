import os
from unittest.mock import patch, MagicMock
from database import models


def test_env_loading_from_project_root(monkeypatch):
    # Ensure BASE_DIR points to project root
    assert os.path.basename(models.BASE_DIR) == "CI-CD-DevOps"


def test_test_connection_success():
    with patch("database.models.engine.connect") as mock_conn:
        ctx = MagicMock()
        ctx.__enter__.return_value = MagicMock()
        mock_conn.return_value = ctx
        assert models.test_connection() is True


def test_test_connection_failure():
    with patch("database.models.engine.connect", side_effect=Exception("boom")):
        assert models.test_connection() is False
