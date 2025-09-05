import pytest
from unittest.mock import patch, Mock
import os

from foundaudio.tools.get_audio_list import get_audio_list
from arcade_core.errors import ToolExecutionError
from arcade_tdk import ToolContext


def test_get_audio_list_basic():
    """Test basic functionality without filters."""
    with patch('foundaudio.tools.get_audio_list.os.getenv') as mock_getenv, \
         patch('foundaudio.tools.get_audio_list.create_client') as mock_create_client:
        
        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            'SUPABASE_URL': 'https://test.supabase.co'
        }.get(key, default)
        
        # Mock ToolContext
        mock_context = Mock(spec=ToolContext)
        mock_context.get_secret.return_value = 'test-secret-key'
        
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

        result = get_audio_list(mock_context)

        # Result is now a JSON string
        import json
        parsed_result = json.loads(result)
        assert len(parsed_result) == 1
        assert parsed_result[0]["title"] == "Test Track"
        assert parsed_result[0]["genres"] == ["electronic"]


def test_get_audio_list_invalid_limit():
    """Test validation of limit parameter."""
    # Mock ToolContext for validation tests
    mock_context = Mock(spec=ToolContext)
    mock_context.get_secret.return_value = 'test-secret-key'
    
    with pytest.raises(ToolExecutionError, match="Error in execution of GetAudioList"):
        get_audio_list(mock_context, limit=0)

    with pytest.raises(ToolExecutionError, match="Error in execution of GetAudioList"):
        get_audio_list(mock_context, limit=101)