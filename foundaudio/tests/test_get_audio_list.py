import pytest
from unittest.mock import Mock, patch
import os

from foundaudio.tools.get_audio_list import get_audio_list


class TestGetAudioList:
    """Test suite for the get_audio_list tool."""

    def setup_method(self):
        """Set up test environment before each test."""
        self.original_env = os.environ.copy()
        os.environ["SUPABASE_ANON_KEY"] = "sb_publishable_4L_ms4VzC-6HXYgq90P3Nw_1AGhi3Hm"
        os.environ["SUPABASE_URL"] = "https://test.supabase.co"

    def teardown_method(self):
        """Clean up after each test."""
        os.environ.clear()
        os.environ.update(self.original_env)

    @patch('foundaudio.tools.get_audio_list.create_client')
    def test_get_audio_list_basic(self, mock_create_client):
        """Test basic functionality without filters."""
        mock_client = Mock()
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
        mock_client.from.return_value.select.return_value.order.return_value.limit.return_value.execute.return_value = mock_response
        mock_create_client.return_value = mock_client

        result = get_audio_list()

        assert len(result) == 1
        assert result[0]["title"] == "Test Track"
        assert result[0]["genres"] == ["electronic"]

    @patch('foundaudio.tools.get_audio_list.create_client')
    def test_get_audio_list_with_search(self, mock_create_client):
        """Test search functionality."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.data = []
        query_chain = mock_client.from.return_value.select.return_value
        query_chain.or_.return_value.order.return_value.limit.return_value.execute.return_value = mock_response
        mock_create_client.return_value = mock_client

        get_audio_list(search="electronic")

        query_chain.or_.assert_called_once_with("title.ilike.%electronic%,description.ilike.%electronic%")

    @patch('foundaudio.tools.get_audio_list.create_client')
    def test_get_audio_list_with_genre(self, mock_create_client):
        """Test genre filtering."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.data = []
        query_chain = mock_client.from.return_value.select.return_value
        query_chain.contains.return_value.order.return_value.limit.return_value.execute.return_value = mock_response
        mock_create_client.return_value = mock_client

        get_audio_list(genre="rock")

        query_chain.contains.assert_called_once_with("genres", ["rock"])

    def test_get_audio_list_invalid_limit(self):
        """Test validation of limit parameter."""
        with pytest.raises(ValueError, match="Limit must be between 1 and 100"):
            get_audio_list(limit=0)

        with pytest.raises(ValueError, match="Limit must be between 1 and 100"):
            get_audio_list(limit=101)

    def test_get_audio_list_missing_supabase_key(self):
        """Test error when SUPABASE_ANON_KEY is missing."""
        del os.environ["SUPABASE_ANON_KEY"]

        with pytest.raises(RuntimeError, match="SUPABASE_ANON_KEY environment variable is required"):
            get_audio_list()

    @patch('foundaudio.tools.get_audio_list.create_client')
    def test_get_audio_list_empty_response(self, mock_create_client):
        """Test handling of empty response."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.data = None
        query_chain = mock_client.from.return_value.select.return_value
        query_chain.order.return_value.limit.return_value.execute.return_value = mock_response
        mock_create_client.return_value = mock_client

        result = get_audio_list()
        assert result == []

    @patch('foundaudio.tools.get_audio_list.create_client')
    def test_get_audio_list_error_handling(self, mock_create_client):
        """Test error handling."""
        mock_client = Mock()
        query_chain = mock_client.from.return_value.select.return_value
        query_chain.order.return_value.limit.return_value.execute.side_effect = Exception("Database error")
        mock_create_client.return_value = mock_client

        with pytest.raises(RuntimeError, match="Error getting audio list: Database error"):
            get_audio_list()
