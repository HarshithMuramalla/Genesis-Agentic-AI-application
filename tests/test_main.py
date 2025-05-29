import pytest
from fastapi.testclient import TestClient
import sys
import os
import json
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from unittest.mock import Mock, patch

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from main import app

client = TestClient(app)

def test_read_root():
    """Test the root endpoint returns the frontend HTML"""
    with patch('os.path.exists') as mock_exists:
        mock_exists.return_value = True
        response = client.get("/")
        assert response.status_code == 200

def test_send_email_success():
    """Test successful email sending with Ollama enhancement"""
    with patch('main.get_google_creds') as mock_creds, \
         patch('main.build') as mock_build, \
         patch('requests.post') as mock_post:
        # Mock the Ollama API response
        mock_response = Mock()
        mock_response.iter_lines.return_value = [b'{"response": "Enhanced email content"}']
        mock_post.return_value = mock_response
        
        # Mock Gmail service
        mock_service = Mock()
        mock_build.return_value = mock_service
        mock_service.users().messages().send().execute.return_value = {}
        
        email_request = {
            "to": "test@example.com",
            "subject": "Test Subject",
            "message": "Test Message"
        }
        
        response = client.post("/send-email", json=email_request)
        assert response.status_code == 200
        assert response.json() == {"message": "Email sent successfully"}

def test_schedule_meeting_success():
    """Test successful meeting scheduling with Ollama enhancement"""
    with patch('main.get_google_creds') as mock_creds, \
         patch('main.build') as mock_build, \
         patch('requests.post') as mock_post:
        # Mock the Ollama API response
        mock_response = Mock()
        mock_response.iter_lines.return_value = [b'{"response": "Enhanced description"}']
        mock_post.return_value = mock_response
        
        # Mock Calendar service
        mock_service = Mock()
        mock_build.return_value = mock_service
        mock_service.events().insert().execute.return_value = {
            "id": "test_event_id",
            "htmlLink": "https://calendar.google.com/test"
        }
        
        calendar_request = {
            "summary": "Test Meeting",
            "description": "Test Description",
            "start_time": "2025-05-28T10:00:00",
            "end_time": "2025-05-28T11:00:00"
        }
        
        response = client.post("/schedule-meeting", json=calendar_request)
        assert response.status_code == 200
        assert response.json()["message"] == "Meeting scheduled successfully"
        assert "event" in response.json()

def test_search_youtube_success():
    """Test successful YouTube search with Ollama enhancement"""
    with patch('main.get_google_creds') as mock_creds, \
         patch('main.build') as mock_build, \
         patch('requests.post') as mock_post:
        # Mock the Ollama API response
        mock_response = Mock()
        mock_response.iter_lines.return_value = [b'{"response": "Enhanced search query"}']
        mock_post.return_value = mock_response
        
        # Mock YouTube service
        mock_service = Mock()
        mock_build.return_value = mock_service
        mock_service.search().list().execute.return_value = {
            "items": [
                {
                    "id": {"videoId": "test_video_id"},
                    "snippet": {"title": "Test Video"}
                }
            ]
        }
        
        youtube_request = {
            "query": "test search"
        }
        
        response = client.post("/search-youtube", json=youtube_request)
        assert response.status_code == 200
        assert "results" in response.json()

def test_google_creds_error():
    """Test error handling when Google credentials fail"""
    with patch('main.get_google_creds') as mock_creds:
        mock_creds.side_effect = Exception("Authentication failed")
        
        email_request = {
            "to": "test@example.com",
            "subject": "Test Subject",
            "message": "Test Message"
        }
        
        response = client.post("/send-email", json=email_request)
        assert response.status_code == 500
        assert "detail" in response.json()
        assert "Authentication failed" in response.json()["detail"]

def test_ollama_service_error():
    """Test error handling when Ollama service is not available"""
    with patch('main.get_google_creds') as mock_creds, \
         patch('main.build') as mock_build, \
         patch('requests.post') as mock_post:
        mock_post.side_effect = requests.exceptions.ConnectionError("Failed to connect to Ollama")
        
        email_request = {
            "to": "test@example.com",
            "subject": "Test Subject",
            "message": "Test Message"
        }
        
        response = client.post("/send-email", json=email_request)
        assert response.status_code == 500
        assert "detail" in response.json()
