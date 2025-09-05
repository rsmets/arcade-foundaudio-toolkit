import pytest
from unittest.mock import patch, Mock
import os

from foundaudio.tools.get_audio_list import get_audio_list
from arcade_core.errors import ToolExecutionError


def test_get_audio_list_basic():
    """Test basic functionality without filters."""
    with patch('foundaudio.tools.get_audio_list.os.getenv') as mock_getenv, \
         patch('foundaudio.tools.get_audio_list.create_client') as mock_create_client:
        
        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            'SUPABASE_URL': 'https://test.supabase.co',
            'SUPABASE_ANON_KEY': 'test-key'
        }.get(key, default)
        
        # Mock Supabase client
        mock_client = mock_create_client.return_value
        mock_response = Mock()
        mock_response.data = [
            {
                "id": "123",
                "title": "Test Track",
                "description": "A test track",
                "file_path": "audio/test.mp3",
                "duration": 180.5,
                "genres": ["electronic"],
                "user_id": "user123",
                "created_at": "2024-01-01T00:00:00Z",
                "profiles": {"email": "test@example.com", "username": "testuser"}
            }
        ]
        
        query_mock = Mock()
        query_mock.order.return_value.limit.return_value.execute.return_value = mock_response
        mock_client.from_.return_value.select.return_value = query_mock

        result = get_audio_list()

        assert len(result) == 1
        assert result[0]["title"] == "Test Track"
        assert result[0]["genres"] == ["electronic"]


def test_get_audio_list_invalid_limit():
    """Test validation of limit parameter."""
    with pytest.raises(ToolExecutionError, match="Error in execution of GetAudioList"):
        get_audio_list(limit=0)

    with pytest.raises(ToolExecutionError, match="Error in execution of GetAudioList"):
        get_audio_list(limit=101)