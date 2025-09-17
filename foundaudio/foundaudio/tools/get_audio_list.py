import os
from typing import Annotated, Any, Dict, List, Optional

from arcade_core.errors import RetryableToolError, ToolExecutionError
from arcade_tdk import ToolContext, tool
from pydantic import BaseModel
from supabase import create_client


class AudioFile(BaseModel):
    """Audio file metadata structure."""

    id: str
    title: str
    description: Optional[str] = None
    url: str
    duration: Optional[float] = None
    genres: List[str] = []
    user_id: str
    created_at: str
    updated_at: str


# NOTE: the Supabase [anon key](https://supabase.com/docs/guides/api/api-keys#anon-and-publishable-keys) is actually not a secret!
# The secret ToolContext was used as a placeholder to show how to properly handle secrets in the toolkit.
@tool(requires_secrets=["SUPABASE_ANON_KEY"])
def get_audio_list(
    context: ToolContext,
    limit: Annotated[
        Optional[int], "Number of audio files to return (default: 20, max: 100)"
    ] = 20,
    search: Annotated[
        Optional[str],
        "Search term to filter by title or description. Leave empty to get all audio files.",
    ] = None,
    genre: Annotated[Optional[str], "Genre to filter by"] = None,
    username: Annotated[
        Optional[str],
        "Username to filter audio files by specific user. If provided, only returns audio files from this user.",
    ] = None,
) -> Dict[str, Any]:
    """Get a list of audio files from the Found Audio database.

    This tool retrieves audio files with optional filtering by search term, genre, or username.
    When a username is provided, it first looks up the user ID from the profiles table,
    then filters audio files to only show those belonging to that user.
    It returns basic audio file information including title, description, duration, and metadata.

    Args:
        limit: Number of audio files to return (default: 20, max: 100)
        search: Optional search term to filter by title or description
        genre: Optional genre to filter by
        username: Optional username to filter audio files by specific user

    Returns:
        A dictionary containing the audio files list and metadata

    Raises:
        RetryableToolError: If there's a recoverable error (e.g., invalid parameters, username not found)
        ToolExecutionError: If there's an unrecoverable error (e.g., missing configuration)
    """
    # Validate limit parameter - use RetryableToolError for parameter validation
    if limit is not None and (limit < 1 or limit > 100):
        raise RetryableToolError(
            "Invalid limit parameter. Please provide a limit between 1 and 100.",
            additional_prompt_content="The limit parameter must be between 1 and 100. Please adjust your request.",
        )

    # Validate username parameter if provided
    if username is not None and (not username.strip()):
        raise RetryableToolError(
            "Invalid username parameter. Username cannot be empty.",
            additional_prompt_content="Please provide a valid username or leave it empty to search all users.",
        )

    try:
        # Get Supabase configuration
        supabase_url = os.getenv(
            "SUPABASE_URL", "https://msocrbprgpaqvrtrcqpo.supabase.co"
        )
        supabase_key = context.get_secret("SUPABASE_ANON_KEY")

        if not supabase_key:
            raise ToolExecutionError("SUPABASE_ANON_KEY secret is not configured")

        # Create Supabase client
        supabase = create_client(supabase_url, supabase_key)

        # Look up user ID if username is provided
        # NOTE: This is where some complexity of dealing with intent-based implementation comes in
        user_id = None
        if username and username.strip():
            try:
                # Query the profiles table to get user ID by username
                # Using the exact API pattern from the user's example
                # Select all fields to match the actual response structure
                profile_response = (
                    supabase.from_("profiles")
                    .select("id, username, email, created_at")
                    .eq("username", username.strip())
                    .execute()
                )

                if not profile_response.data or len(profile_response.data) == 0:
                    raise RetryableToolError(
                        f"Username '{username}' not found. Please check the username and try again.",
                        additional_prompt_content=f"The username '{username}' does not exist in the system. Please verify the username is correct.",
                    )

                # Extract user ID from the first (and should be only) result
                # The response structure is: [{"id": "uuid", "username": "discodude", "email": "...", "created_at": "..."}]
                user_id = profile_response.data[0]["id"]

            except RetryableToolError:
                # Re-raise RetryableToolError as-is (username not found)
                raise
            except Exception as e:
                # For unexpected errors during username lookup, raise ToolExecutionError
                raise ToolExecutionError(
                    f"Error looking up username '{username}': {str(e)}"
                ) from e

        # Build query - select fields that actually exist in the API response
        select_fields = (
            "id, title, description, duration, genres, user_id, created_at, updated_at"
        )
        query = supabase.from_("audio_files").select(select_fields)

        # Apply user ID filter if username was provided and found
        if user_id:
            query = query.eq("user_id", user_id)

        # Apply search filter
        if search and search.strip():
            query = query.or_(f"title.ilike.%{search}%,description.ilike.%{search}%")

        # Apply genre filter
        if genre and genre.strip():
            query = query.contains("genres", [genre])

        # Apply ordering and limit
        query = query.order("created_at", desc=True).limit(limit)

        # Execute query
        response = query.execute()

        if response.data is None:
            return {
                "audio_files": [],
                "count": 0,
                "limit": limit,
                "search": search,
                "genre": genre,
                "username": username,
            }

        # Convert the raw data to dictionaries
        audio_files = []
        for item in response.data:
            # Create AudioFile object first for validation
            audio_file = AudioFile(
                id=item["id"],
                title=item["title"],
                description=item.get("description"),
                duration=item.get("duration"),
                genres=item.get("genres", []),
                user_id=item["user_id"],
                created_at=item["created_at"],
                updated_at=item["updated_at"],
                url="https://foundaudio.club/audio/" + item["id"],
            )

            # Convert to dictionary for return
            audio_file_dict = audio_file.model_dump()
            audio_files.append(audio_file_dict)

        return {
            "audio_files": audio_files,
            "count": len(audio_files),
            "limit": limit,
            "search": search,
            "genre": genre,
            "username": username,
        }

    except RetryableToolError:
        # Re-raise RetryableToolError as-is
        raise
    except Exception as e:
        # For unexpected errors, raise ToolExecutionError (will be caught by @tool decorator)
        raise ToolExecutionError(f"Error accessing audio database: {str(e)}") from e
