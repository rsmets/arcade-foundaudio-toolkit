import os
from unittest.mock import Mock, patch

import pytest
from arcade_core.errors import RetryableToolError, ToolExecutionError
from arcade_tdk import ToolContext

from foundaudio.tools.get_audio_list import get_audio_list

# =============================================================================
# NORMAL OPERATION TESTS
# These tests verify the tool works correctly under normal conditions
# =============================================================================


def test_get_audio_list_basic():
    """NORMAL OPERATION: Test basic functionality without filters.

    This test verifies that the tool can successfully retrieve audio files
    from the database without any search or genre filters applied.
    """
    with patch("foundaudio.tools.get_audio_list.os.getenv") as mock_getenv, patch(
        "foundaudio.tools.get_audio_list.create_client"
    ) as mock_create_client:

        # SETUP: Mock environment variables for Supabase configuration
        mock_getenv.side_effect = lambda key, default=None: {
            "SUPABASE_URL": "https://test.supabase.co"
        }.get(key, default)

        # SETUP: Mock ToolContext with valid secret
        mock_context = Mock(spec=ToolContext)
        mock_context.get_secret.return_value = "test-secret-key"

        # SETUP: Mock Supabase client and database response
        mock_client = mock_create_client.return_value
        mock_response = Mock()
        # Simulate database returning one audio file record
        mock_response.data = [
            {
                "id": "123",
                "title": "Test Track",
                "description": "A test track",
                "duration": 180.5,
                "genres": ["electronic"],
                "user_id": "user123",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
            }
        ]

        # SETUP: Mock the Supabase query chain (from -> select -> order -> limit -> execute)
        query_mock = Mock()
        query_mock.order.return_value.limit.return_value.execute.return_value = (
            mock_response
        )
        mock_client.from_.return_value.select.return_value = query_mock

        # EXECUTE: Call the function under test
        result = get_audio_list(mock_context)

        # VERIFY: Check that result has correct structure and data
        # Verify return type is dictionary
        if not isinstance(result, dict):
            raise AssertionError(f"Expected result to be dict, got {type(result)}")
        if "audio_files" not in result:
            raise AssertionError("Expected 'audio_files' key in result")

        # Verify audio_files is a list with expected count
        if not isinstance(result["audio_files"], list):
            raise AssertionError(
                f"Expected audio_files to be list, got {type(result['audio_files'])}"
            )
        if len(result["audio_files"]) != 1:
            raise AssertionError(
                f"Expected 1 audio file, got {len(result['audio_files'])}"
            )

        # Verify individual audio file structure and content
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

        # Verify URL generation - should be generated from ID
        expected_url = "https://foundaudio.club/audio/123"
        if result["audio_files"][0]["url"] != expected_url:
            raise AssertionError(
                f"Expected URL '{expected_url}', got {result['audio_files'][0]['url']}"
            )

        # Verify metadata fields
        if result["count"] != 1:
            raise AssertionError(f"Expected count 1, got {result['count']}")


# =============================================================================
# INPUT VALIDATION TESTS
# These tests verify that invalid inputs are properly validated and rejected
# =============================================================================


def test_get_audio_list_invalid_limit():
    """INPUT VALIDATION: Test validation of limit parameter using RetryableToolError.

    This test verifies that the tool properly validates the limit parameter
    and raises RetryableToolError for values outside the valid range (1-100).
    RetryableToolError indicates the user can retry with corrected input.
    """
    # SETUP: Mock ToolContext for validation tests
    mock_context = Mock(spec=ToolContext)
    mock_context.get_secret.return_value = "test-secret-key"

    # TEST: Verify limit parameter validation - too low (boundary test)
    # Should raise RetryableToolError because user can fix by providing valid limit
    with pytest.raises(RetryableToolError, match="Invalid limit parameter"):
        get_audio_list(mock_context, limit=0)

    # TEST: Verify limit parameter validation - too high (boundary test)
    # Should raise RetryableToolError because user can fix by providing valid limit
    with pytest.raises(RetryableToolError, match="Invalid limit parameter"):
        get_audio_list(mock_context, limit=101)


def test_get_audio_list_no_results():
    """NORMAL OPERATION: Test when no audio files are found.

    This test verifies that the tool gracefully handles the case where
    the database query returns no results, returning an empty list
    rather than failing or returning None.
    """
    with patch("foundaudio.tools.get_audio_list.os.getenv") as mock_getenv, patch(
        "foundaudio.tools.get_audio_list.create_client"
    ) as mock_create_client:

        # SETUP: Mock environment variables for Supabase configuration
        mock_getenv.side_effect = lambda key, default=None: {
            "SUPABASE_URL": "https://test.supabase.co"
        }.get(key, default)

        # SETUP: Mock ToolContext with valid secret
        mock_context = Mock(spec=ToolContext)
        mock_context.get_secret.return_value = "test-secret-key"

        # SETUP: Mock Supabase client with no results
        mock_client = mock_create_client.return_value
        mock_response = Mock()
        mock_response.data = None  # Simulate database returning no results

        # SETUP: Mock the Supabase query chain
        query_mock = Mock()
        query_mock.order.return_value.limit.return_value.execute.return_value = (
            mock_response
        )
        mock_client.from_.return_value.select.return_value = query_mock

        # EXECUTE: Call the function under test
        result = get_audio_list(mock_context)

        # VERIFY: Should return empty result structure instead of None
        # Verify return type is dictionary
        if not isinstance(result, dict):
            raise AssertionError(f"Expected result to be dict, got {type(result)}")
        if "audio_files" not in result:
            raise AssertionError("Expected 'audio_files' key in result")

        # Verify empty results are handled correctly
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


# =============================================================================
# ERROR HANDLING TESTS
# These tests verify proper error handling for system/configuration issues
# =============================================================================


def test_get_audio_list_missing_secret():
    """ERROR HANDLING: Test error handling when secret is missing.

    This test verifies that the tool properly handles missing configuration
    (SUPABASE_ANON_KEY secret) and raises ToolExecutionError for system issues
    that cannot be resolved by the user retrying with different input.
    """
    with patch("foundaudio.tools.get_audio_list.os.getenv") as mock_getenv:

        # SETUP: Mock environment variables for Supabase configuration
        mock_getenv.side_effect = lambda key, default=None: {
            "SUPABASE_URL": "https://test.supabase.co"
        }.get(key, default)

        # SETUP: Mock ToolContext with missing secret (system configuration issue)
        mock_context = Mock(spec=ToolContext)
        mock_context.get_secret.return_value = None  # Simulate missing secret

        # TEST: Verify that missing secret raises ToolExecutionError (not retryable)
        # This is a system/configuration error that user cannot fix by changing input
        with pytest.raises(
            ToolExecutionError,
            match="Error accessing audio database: SUPABASE_ANON_KEY secret is not configured",
        ):
            get_audio_list(mock_context)


def test_get_audio_list_with_filters():
    """NORMAL OPERATION: Test functionality with search and genre filters.

    This test verifies that the tool correctly applies search and genre
    filters to the database query and returns properly filtered results.
    It also tests that the returned metadata includes the applied filters.
    """
    with patch("foundaudio.tools.get_audio_list.os.getenv") as mock_getenv, patch(
        "foundaudio.tools.get_audio_list.create_client"
    ) as mock_create_client:

        # SETUP: Mock environment variables for Supabase configuration
        mock_getenv.side_effect = lambda key, default=None: {
            "SUPABASE_URL": "https://test.supabase.co"
        }.get(key, default)

        # SETUP: Mock ToolContext with valid secret
        mock_context = Mock(spec=ToolContext)
        mock_context.get_secret.return_value = "test-secret-key"

        # SETUP: Mock Supabase client and filtered response
        mock_client = mock_create_client.return_value
        mock_response = Mock()
        # Simulate database returning filtered results matching search and genre
        mock_response.data = [
            {
                "id": "456",
                "title": "House Track",
                "description": "A house music track",
                "duration": 240.0,
                "genres": ["house"],
                "user_id": "user456",
                "created_at": "2024-01-02T00:00:00Z",
                "updated_at": "2024-01-02T00:00:00Z",
            }
        ]

        # SETUP: Create detailed mocks for chained method calls with filters
        query_mock = Mock()
        or_mock = Mock()
        contains_mock = Mock()
        order_mock = Mock()
        limit_mock = Mock()

        # SETUP: Mock the complex query chain with filters: from_ -> select -> or_ -> contains -> order -> limit -> execute
        mock_client.from_.return_value.select.return_value = query_mock
        query_mock.or_.return_value = or_mock
        or_mock.contains.return_value = contains_mock
        contains_mock.order.return_value = order_mock
        order_mock.limit.return_value = limit_mock
        limit_mock.execute.return_value = mock_response

        # EXECUTE: Call the function under test with search and genre filters
        result = get_audio_list(mock_context, limit=10, search="house", genre="house")

        # VERIFY: Check that result has correct structure and filtered data
        # Verify return type is dictionary
        if not isinstance(result, dict):
            raise AssertionError(f"Expected result to be dict, got {type(result)}")
        if "audio_files" not in result:
            raise AssertionError("Expected 'audio_files' key in result")

        # Verify filtered results structure
        if not isinstance(result["audio_files"], list):
            raise AssertionError(
                f"Expected audio_files to be list, got {type(result['audio_files'])}"
            )
        if len(result["audio_files"]) != 1:
            raise AssertionError(
                f"Expected 1 audio file, got {len(result['audio_files'])}"
            )

        # Verify individual audio file content matches filters
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

        # Verify URL generation for filtered results - should be generated from ID
        expected_url = "https://foundaudio.club/audio/456"
        if result["audio_files"][0]["url"] != expected_url:
            raise AssertionError(
                f"Expected URL '{expected_url}', got {result['audio_files'][0]['url']}"
            )

        # Verify metadata fields include applied filters
        if result["count"] != 1:
            raise AssertionError(f"Expected count 1, got {result['count']}")
        if result["limit"] != 10:
            raise AssertionError(f"Expected limit 10, got {result['limit']}")
        if result["search"] != "house":
            raise AssertionError(f"Expected search 'house', got {result['search']}")
        if result["genre"] != "house":
            raise AssertionError(f"Expected genre to be 'house', got {result['genre']}")

        # VERIFY: Check that the correct query methods were called with expected parameters
        query_mock.or_.assert_called_once_with(
            "title.ilike.%house%,description.ilike.%house%"
        )
        or_mock.contains.assert_called_once_with("genres", ["house"])
        contains_mock.order.assert_called_once_with("created_at", desc=True)
        order_mock.limit.assert_called_once_with(10)


def test_get_audio_list_url_generation():
    """NORMAL OPERATION: Test URL generation format and consistency.

    This test verifies that the tool correctly generates URLs for audio files
    using the expected pattern: https://foundaudio.club/audio/{id}
    """
    with patch("foundaudio.tools.get_audio_list.os.getenv") as mock_getenv, patch(
        "foundaudio.tools.get_audio_list.create_client"
    ) as mock_create_client:

        # SETUP: Mock environment variables for Supabase configuration
        mock_getenv.side_effect = lambda key, default=None: {
            "SUPABASE_URL": "https://test.supabase.co"
        }.get(key, default)

        # SETUP: Mock ToolContext with valid secret
        mock_context = Mock(spec=ToolContext)
        mock_context.get_secret.return_value = "test-secret-key"

        # SETUP: Mock Supabase client with multiple audio files to test URL generation
        mock_client = mock_create_client.return_value
        mock_response = Mock()
        # Simulate database returning multiple audio files with different IDs
        mock_response.data = [
            {
                "id": "abc123",
                "title": "Track One",
                "description": "First test track",
                "duration": 120.0,
                "genres": ["rock"],
                "user_id": "user1",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
            },
            {
                "id": "xyz789",
                "title": "Track Two",
                "description": "Second test track",
                "duration": 180.0,
                "genres": ["jazz"],
                "user_id": "user2",
                "created_at": "2024-01-02T00:00:00Z",
                "updated_at": "2024-01-02T00:00:00Z",
            },
        ]

        # SETUP: Mock the Supabase query chain
        query_mock = Mock()
        query_mock.order.return_value.limit.return_value.execute.return_value = (
            mock_response
        )
        mock_client.from_.return_value.select.return_value = query_mock

        # EXECUTE: Call the function under test
        result = get_audio_list(mock_context)

        # VERIFY: Check that URLs are generated correctly for each audio file
        if not isinstance(result, dict) or "audio_files" not in result:
            raise AssertionError("Expected result with audio_files key")

        audio_files = result["audio_files"]
        if len(audio_files) != 2:
            raise AssertionError(f"Expected 2 audio files, got {len(audio_files)}")

        # Verify URL format for first audio file
        expected_url_1 = "https://foundaudio.club/audio/abc123"
        if audio_files[0]["url"] != expected_url_1:
            raise AssertionError(
                f"Expected URL '{expected_url_1}', got {audio_files[0]['url']}"
            )

        # Verify URL format for second audio file
        expected_url_2 = "https://foundaudio.club/audio/xyz789"
        if audio_files[1]["url"] != expected_url_2:
            raise AssertionError(
                f"Expected URL '{expected_url_2}', got {audio_files[1]['url']}"
            )

        # Verify that URLs follow the expected pattern (base URL + ID)
        base_url = "https://foundaudio.club/audio/"
        for i, audio_file in enumerate(audio_files):
            if not audio_file["url"].startswith(base_url):
                raise AssertionError(
                    f"Expected URL to start with '{base_url}', got {audio_file['url']}"
                )
            # Extract ID from URL and verify it matches the original ID
            url_id = audio_file["url"].replace(base_url, "")
            expected_id = mock_response.data[i]["id"]
            if url_id != expected_id:
                raise AssertionError(
                    f"Expected URL to contain ID '{expected_id}', got '{url_id}'"
                )
