import pytest
import os
import json

@pytest.fixture
def mock_credentials_file(tmp_path):
    """Create a mock credentials file for testing"""
    creds = {
        "installed": {
            "client_id": "test_client_id",
            "client_secret": "test_client_secret",
            "redirect_uris": ["http://localhost"]
        }
    }
    creds_file = tmp_path / "credentials.json"
    with open(creds_file, "w") as f:
        json.dump(creds, f)
    return str(creds_file)

@pytest.fixture
def mock_token_file(tmp_path):
    """Create a mock token file for testing"""
    token = {
        "token": "test_token",
        "refresh_token": "test_refresh_token",
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": "test_client_id",
        "client_secret": "test_client_secret",
        "scopes": ["https://www.googleapis.com/auth/gmail.send"]
    }
    token_file = tmp_path / "token.json"
    with open(token_file, "w") as f:
        json.dump(token, f)
    return str(token_file)
