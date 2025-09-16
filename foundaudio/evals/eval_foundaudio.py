from arcade_evals import (
    BinaryCritic,
    EvalRubric,
    EvalSuite,
    ExpectedToolCall,
    NumericCritic,
    SimilarityCritic,
    tool_eval,
)
from arcade_tdk import ToolCatalog

import foundaudio
from foundaudio.tools.get_audio_list import get_audio_list


# Safely clean text fields for critics
def clean_text(text: str | None) -> str:
    return str(text).lower() if text is not None else ""


# Evaluation rubric with appropriate thresholds for audio search tool
rubric = EvalRubric(
    fail_threshold=0.8,  # Slightly lower threshold for complex audio search scenarios
    warn_threshold=0.9,
)

# Create a catalog of tools to include in the evaluation
catalog = ToolCatalog()
catalog.add_module(foundaudio)


@tool_eval()
def foundaudio_eval_suite() -> EvalSuite:
    """Create a comprehensive evaluation suite for the foundaudio audio search tool.

    This evaluation suite tests the get_audio_list tool with various scenarios
    including basic functionality, filtering, parameter validation, edge cases,
    and error handling.
    """
    suite = EvalSuite(
        name="Found Audio Search Tool Evaluation Suite",
        system_message=(
            "You are an AI assistant with access to foundaudio tools. "
            "You can search for audio files using various filters. Use the "
            "get_audio_list tool to help users find audio content."
        ),
        catalog=catalog,
        rubric=rubric,
    )

    # =============================================================================
    # GET_AUDIO_LIST TOOL EVALUATIONS - BASIC FUNCTIONALITY
    # =============================================================================

    suite.add_case(
        name="Basic Audio Search - No Filters",
        user_message="Show me some audio files",
        expected_tool_calls=[
            ExpectedToolCall(
                func=get_audio_list,
                args={},  # No parameters - should use defaults
            )
        ],
        critics=[
            # No specific field critics needed for basic call
        ],
    )

    suite.add_case(
        name="Audio Search with Limit",
        user_message="Show me 5 audio files",
        expected_tool_calls=[
            ExpectedToolCall(
                func=get_audio_list,
                args={"limit": 5},
            )
        ],
        critics=[
            NumericCritic(
                critic_field="limit",
                weight=1.0,
                value_range=(1, 100),
                match_threshold=1.0,
            ),
        ],
    )

    suite.add_case(
        name="Audio Search with Search Term",
        user_message="Find audio files about jazz music",
        expected_tool_calls=[
            ExpectedToolCall(
                func=get_audio_list,
                args={"search": "jazz"},
            )
        ],
        critics=[
            SimilarityCritic(
                critic_field="search",
                weight=1.0,
                cleaning_func=lambda s: clean_text(s),
            ),
        ],
    )

    suite.add_case(
        name="Audio Search with Genre Filter",
        user_message="Show me electronic music tracks",
        expected_tool_calls=[
            ExpectedToolCall(
                func=get_audio_list,
                args={"genre": "electronic"},
            )
        ],
        critics=[
            SimilarityCritic(
                critic_field="genre",
                weight=1.0,
                cleaning_func=lambda s: clean_text(s),
            ),
        ],
    )

    # =============================================================================
    # GET_AUDIO_LIST TOOL EVALUATIONS - COMBINED FILTERS
    # =============================================================================

    suite.add_case(
        name="Audio Search with Multiple Filters",
        user_message="Find 10 house music mixes with 'dance' in the title",
        expected_tool_calls=[
            ExpectedToolCall(
                func=get_audio_list,
                args={
                    "limit": 10,
                    "search": "dance",
                    "genre": "house",
                },
            )
        ],
        critics=[
            NumericCritic(
                critic_field="limit",
                weight=0.33,
                value_range=(1, 100),
                match_threshold=1.0,
            ),
            SimilarityCritic(
                critic_field="search",
                weight=0.33,
                cleaning_func=lambda s: clean_text(s),
            ),
            SimilarityCritic(
                critic_field="genre",
                weight=0.34,
                cleaning_func=lambda s: clean_text(s),
            ),
        ],
    )

    suite.add_case(
        name="Audio Search with Partial Search Term",
        user_message="Look for tracks containing 'party' in the description",
        expected_tool_calls=[
            ExpectedToolCall(
                func=get_audio_list,
                args={"search": "party"},
            )
        ],
        critics=[
            SimilarityCritic(
                critic_field="search",
                weight=1.0,
                cleaning_func=lambda s: clean_text(s),
            ),
        ],
    )

    # =============================================================================
    # GET_AUDIO_LIST TOOL EVALUATIONS - PARAMETER VALIDATION
    # =============================================================================

    suite.add_case(
        name="Audio Search with Maximum Limit",
        user_message="Show me the maximum number of audio files (100)",
        expected_tool_calls=[
            ExpectedToolCall(
                func=get_audio_list,
                args={"limit": 100},
            )
        ],
        critics=[
            NumericCritic(
                critic_field="limit",
                weight=1.0,
                value_range=(1, 100),
                match_threshold=1.0,
            ),
        ],
    )

    suite.add_case(
        name="Audio Search with Minimum Limit",
        user_message="Show me just 1 audio file",
        expected_tool_calls=[
            ExpectedToolCall(
                func=get_audio_list,
                args={"limit": 1},
            )
        ],
        critics=[
            NumericCritic(
                critic_field="limit",
                weight=1.0,
                value_range=(1, 100),
                match_threshold=1.0,
            ),
        ],
    )

    # =============================================================================
    # GET_AUDIO_LIST TOOL EVALUATIONS - EDGE CASES
    # =============================================================================

    suite.add_case(
        name="Audio Search with Empty Search Term",
        user_message="Search for audio files with an empty search term",
        expected_tool_calls=[
            ExpectedToolCall(
                func=get_audio_list,
                args={"search": ""},
            )
        ],
        critics=[
            BinaryCritic(critic_field="search", weight=1.0),
        ],
    )

    suite.add_case(
        name="Audio Search with Special Characters",
        user_message="Find audio files with 'rock & roll' in the title",
        expected_tool_calls=[
            ExpectedToolCall(
                func=get_audio_list,
                args={"search": "rock & roll"},
            )
        ],
        critics=[
            SimilarityCritic(
                critic_field="search",
                weight=1.0,
                cleaning_func=lambda s: clean_text(s),
            ),
        ],
    )

    # =============================================================================
    # GET_AUDIO_LIST TOOL EVALUATIONS - COMPLEX SCENARIOS
    # =============================================================================

    suite.add_case(
        name="Audio Search with Multiple Genres Context",
        user_message="I'm looking for some ambient electronic music to study to",
        expected_tool_calls=[
            ExpectedToolCall(
                func=get_audio_list,
                args={"search": "ambient", "genre": "electronic"},
            )
        ],
        critics=[
            SimilarityCritic(
                critic_field="search",
                weight=0.5,
                cleaning_func=lambda s: clean_text(s),
            ),
            SimilarityCritic(
                critic_field="genre",
                weight=0.5,
                cleaning_func=lambda s: clean_text(s),
            ),
        ],
    )

    suite.add_case(
        name="Audio Search with Specific Artist Context",
        user_message="I want to find tracks by a specific artist named 'DJ Sample'",
        expected_tool_calls=[
            ExpectedToolCall(
                func=get_audio_list,
                args={"search": "DJ Sample"},
            )
        ],
        critics=[
            SimilarityCritic(
                critic_field="search",
                weight=1.0,
                cleaning_func=lambda s: clean_text(s),
            ),
        ],
    )

    suite.add_case(
        name="Audio Search with Duration Context",
        user_message="I need short tracks under 2 minutes for my podcast intro",
        expected_tool_calls=[
            ExpectedToolCall(
                func=get_audio_list,
                args={},  # Duration filtering not implemented, should return all
            )
        ],
        critics=[
            # No specific critics since duration filtering isn't implemented
        ],
    )

    # =============================================================================
    # GET_AUDIO_LIST TOOL EVALUATIONS - CONVERSATION CONTEXT
    # =============================================================================

    suite.add_case(
        name="Audio Search with Conversation History",
        user_message="Can you find more tracks like that?",
        expected_tool_calls=[
            ExpectedToolCall(
                func=get_audio_list,
                args={"genre": "jazz"},
            )
        ],
        critics=[
            SimilarityCritic(
                critic_field="genre",
                weight=1.0,
                cleaning_func=lambda s: clean_text(s),
            ),
        ],
        additional_messages=[
            {"role": "user", "content": "I'm looking for jazz music"},
            {"role": "assistant", "content": "I found some great jazz tracks for you!"},
        ],
    )

    suite.add_case(
        name="Audio Search with User Preference Context",
        user_message="Show me more of those",
        expected_tool_calls=[
            ExpectedToolCall(
                func=get_audio_list,
                args={"search": "electronic", "genre": "house"},
            )
        ],
        critics=[
            SimilarityCritic(
                critic_field="search",
                weight=0.5,
                cleaning_func=lambda s: clean_text(s),
            ),
            SimilarityCritic(
                critic_field="genre",
                weight=0.5,
                cleaning_func=lambda s: clean_text(s),
            ),
        ],
        additional_messages=[
            {"role": "user", "content": "I love electronic house music"},
            {"role": "assistant", "content": "Here are some electronic house tracks!"},
        ],
    )

    # =============================================================================
    # GET_AUDIO_LIST TOOL EVALUATIONS - ERROR SCENARIOS
    # =============================================================================

    suite.add_case(
        name="Audio Search with Invalid Limit - Too High",
        user_message="Show me 150 audio files",
        expected_tool_calls=[],  # None because RetryableToolError is raised
        critics=[],
    )

    suite.add_case(
        name="Audio Search with Invalid Limit - Too Low",
        user_message="Show me 0 audio files",
        expected_tool_calls=[],
        critics=[],
    )

    return suite
