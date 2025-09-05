import os
from unittest.mock import Mock, patch

import pytest
from arcade_core.errors import RetryableToolError, ToolExecutionError
from arcade_tdk import ToolContext

from foundaudio.tools.get_audio_list import get_audio_list


def test_get_audio_list_basic():
    """Test basic functionality without filters."""
    with patch("foundaudio.tools.get_audio_list.os.getenv") as mock_getenv, patch(
        "foundaudio.tools.get_audio_list.create_client"
    ) as mock_create_client:

        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            "SUPABASE_URL": "https://test.supabase.co"
        }.get(key, default)

        # Mock ToolContext
        mock_context = Mock(spec=ToolContext)
        mock_context.get_secret.return_value = "test-secret-key"

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
                "updated_at": "2024-01-01T00:00:00Z",
            }
        ]

        query_mock = Mock()
        query_mock.order.return_value.limit.return_value.execute.return_value = (
            mock_response
        )
        mock_client.from_.return_value.select.return_value = query_mock

        result = get_audio_list(mock_context)

        # Result is now a dictionary containing audio files
        if not isinstance(result, dict):
            raise AssertionError(f"Expected result to be dict, got {type(result)}")
        if "audio_files" not in result:
            raise AssertionError("Expected 'audio_files' key in result")
        if not isinstance(result["audio_files"], list):
            raise AssertionError(
                f"Expected audio_files to be list, got {type(result['audio_files'])}"
            )
        if len(result["audio_files"]) != 1:
            raise AssertionError(
                f"Expected 1 audio file, got {len(result['audio_files'])}"
            )
        if not isinstance(result["audio_files"][0], dict):
            raise AssertionError(
                f"Expected audio file to be dict, got {type(result['audio_files'][0])}"
            )
        if result["audio_files"][0]["title"] != "Test Track":
            raise AssertionError(
                f"Expected title 'Test Track', got {result['audio_files'][0]['title']}"
            )
        if result["audio_files"][0]["genres"] != ["electronic"]:
            raise AssertionError(
                f"Expected genres ['electronic'], got {result['audio_files'][0]['genres']}"
            )
        if result["audio_files"][0]["updated_at"] != "2024-01-01T00:00:00Z":
            raise AssertionError(
                f"Expected updated_at '2024-01-01T00:00:00Z', got {result['audio_files'][0]['updated_at']}"
            )
        if result["count"] != 1:
            raise AssertionError(f"Expected count 1, got {result['count']}")


def test_get_audio_list_invalid_limit():
    """Test validation of limit parameter using RetryableToolError."""
    # Mock ToolContext for validation tests
    mock_context = Mock(spec=ToolContext)
    mock_context.get_secret.return_value = "test-secret-key"

    # Test limit too low
    with pytest.raises(RetryableToolError, match="Invalid limit parameter"):
        get_audio_list(mock_context, limit=0)

    # Test limit too high
    with pytest.raises(RetryableToolError, match="Invalid limit parameter"):
        get_audio_list(mock_context, limit=101)


def test_get_audio_list_no_results():
    """Test when no audio files are found."""
    with patch("foundaudio.tools.get_audio_list.os.getenv") as mock_getenv, patch(
        "foundaudio.tools.get_audio_list.create_client"
    ) as mock_create_client:

        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            "SUPABASE_URL": "https://test.supabase.co"
        }.get(key, default)

        # Mock ToolContext
        mock_context = Mock(spec=ToolContext)
        mock_context.get_secret.return_value = "test-secret-key"

        # Mock Supabase client with no results
        mock_client = mock_create_client.return_value
        mock_response = Mock()
        mock_response.data = None  # No results

        query_mock = Mock()
        query_mock.order.return_value.limit.return_value.execute.return_value = (
            mock_response
        )
        mock_client.from_.return_value.select.return_value = query_mock

        result = get_audio_list(mock_context)

        # Should return empty result structure instead of None
        if not isinstance(result, dict):
            raise AssertionError(f"Expected result to be dict, got {type(result)}")
        if "audio_files" not in result:
            raise AssertionError("Expected 'audio_files' key in result")
        if not isinstance(result["audio_files"], list):
            raise AssertionError(
                f"Expected audio_files to be list, got {type(result['audio_files'])}"
            )
        if len(result["audio_files"]) != 0:
            raise AssertionError(
                f"Expected 0 audio files, got {len(result['audio_files'])}"
            )
        if result["count"] != 0:
            raise AssertionError(f"Expected count 0, got {result['count']}")


def test_get_audio_list_missing_secret():
    """Test error handling when secret is missing."""
    with patch("foundaudio.tools.get_audio_list.os.getenv") as mock_getenv:

        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            "SUPABASE_URL": "https://test.supabase.co"
        }.get(key, default)

        # Mock ToolContext with missing secret
        mock_context = Mock(spec=ToolContext)
        mock_context.get_secret.return_value = None  # Missing secret

        with pytest.raises(
            ToolExecutionError, match="Error in execution of GetAudioList"
        ):
            get_audio_list(mock_context)


def test_get_audio_list_with_filters():
    """Test functionality with search and genre filters."""
    with patch("foundaudio.tools.get_audio_list.os.getenv") as mock_getenv, patch(
        "foundaudio.tools.get_audio_list.create_client"
    ) as mock_create_client:

        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            "SUPABASE_URL": "https://test.supabase.co"
        }.get(key, default)

        # Mock ToolContext
        mock_context = Mock(spec=ToolContext)
        mock_context.get_secret.return_value = "test-secret-key"

        # Mock Supabase client
        mock_client = mock_create_client.return_value
        mock_response = Mock()
        mock_response.data = [
            {
                "id": "456",
                "title": "House Track",
                "description": "A house music track",
                "file_path": "audio/house.mp3",
                "duration": 240.0,
                "genres": ["house"],
                "user_id": "user456",
                "created_at": "2024-01-02T00:00:00Z",
                "updated_at": "2024-01-02T00:00:00Z",
            }
        ]

        # Create a more detailed mock for chained method calls
        query_mock = Mock()
        or_mock = Mock()
        contains_mock = Mock()
        order_mock = Mock()
        limit_mock = Mock()

        # Set up the chain: from_ -> select -> or_ -> contains -> order -> limit -> execute
        mock_client.from_.return_value.select.return_value = query_mock
        query_mock.or_.return_value = or_mock
        or_mock.contains.return_value = contains_mock
        contains_mock.order.return_value = order_mock
        order_mock.limit.return_value = limit_mock
        limit_mock.execute.return_value = mock_response

        result = get_audio_list(mock_context, limit=10, search="house", genre="house")

        # Verify the result
        if not isinstance(result, dict):
            raise AssertionError(f"Expected result to be dict, got {type(result)}")
        if "audio_files" not in result:
            raise AssertionError("Expected 'audio_files' key in result")
        if not isinstance(result["audio_files"], list):
            raise AssertionError(
                f"Expected audio_files to be list, got {type(result['audio_files'])}"
            )
        if len(result["audio_files"]) != 1:
            raise AssertionError(
                f"Expected 1 audio file, got {len(result['audio_files'])}"
            )
        if not isinstance(result["audio_files"][0], dict):
            raise AssertionError(
                f"Expected audio file to be dict, got {type(result['audio_files'][0])}"
            )
        if result["audio_files"][0]["title"] != "House Track":
            raise AssertionError(
                f"Expected title 'House Track', got {result['audio_files'][0]['title']}"
            )
        if result["audio_files"][0]["genres"] != ["house"]:
            raise AssertionError(
                f"Expected genres ['house'], got {result['audio_files'][0]['genres']}"
            )
        if result["audio_files"][0]["updated_at"] != "2024-01-02T00:00:00Z":
            raise AssertionError(
                f"Expected updated_at '2024-01-02T00:00:00Z', got {result['audio_files'][0]['updated_at']}"
            )
        if result["count"] != 1:
            raise AssertionError(f"Expected count 1, got {result['count']}")
        if result["limit"] != 10:
            raise AssertionError(f"Expected limit 10, got {result['limit']}")
        if result["search"] != "house":
            raise AssertionError(f"Expected search 'house', got {result['search']}")
        if result["genre"] != "house":
            raise AssertionError(f"Expected genre to be 'house', got {result['genre']}")

        # Verify the query methods were called with correct parameters
        query_mock.or_.assert_called_once_with(
            "title.ilike.%house%,description.ilike.%house%"
        )
        or_mock.contains.assert_called_once_with("genres", ["house"])
        contains_mock.order.assert_called_once_with("created_at", desc=True)
        order_mock.limit.assert_called_once_with(10)
