from typing import Annotated, List, Optional, Dict
from supabase import create_client, Client
import os

from arcade_tdk import tool, ToolContext

# NOTE: the supabase key is actually not a secret!
# It is meant to be used in the browser and thus is public. The secret context was used as a placeholder to show how to properly handle secrets in the toolkit.
@tool(requires_secrets=["SUPABASE_ANON_KEY"])
def get_audio_list(
    context: ToolContext,
    limit: Annotated[Optional[int], "Number of audio files to return (default: 20, max: 100)"] = 20,
    search: Annotated[Optional[str], "Search term to filter by title or description"] = None,
    genre: Annotated[Optional[str], "Genre to filter by"] = None
) -> str:
    """Get a list of audio files from the Found Audio database.
    
    This tool retrieves audio files with optional filtering by search term or genre.
    It returns basic audio file information including title, description, duration, and metadata.
    
    Args:
        limit: Number of audio files to return (default: 20, max: 100)
        search: Optional search term to filter by title or description
        genre: Optional genre to filter by
        
    Returns:
        A list of audio file dictionaries with basic information
        
    Raises:
        RuntimeError: If there's an error connecting to the database
    """
    try:
        # Validate limit
        if limit is not None and (limit < 1 or limit > 100):
            raise ValueError("Limit must be between 1 and 100")
        
        # Get Supabase configuration
        supabase_url = os.getenv("SUPABASE_URL", "https://msocrbprgpaqvrtrcqpo.supabase.co")
        supabase_key = context.get_secret("SUPABASE_ANON_KEY")
        
        # Create Supabase client
        supabase = create_client(supabase_url, supabase_key)
        
        # Build query
        select_fields = "id, title, description, file_path, duration, genres, user_id, created_at, profiles (email, username)"
        query = supabase.from_("audio_files").select(select_fields)
        
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
            return "No audio files found."
        
        # Format the results as a readable string
        import json
        return json.dumps(response.data, indent=2)
        
    except Exception as e:
        raise RuntimeError(f"Error getting audio list: {str(e)}")