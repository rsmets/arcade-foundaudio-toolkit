from arcade_evals import (
    BinaryCritic,
    EvalRubric,
    EvalSuite,
    ExpectedToolCall,
    SimilarityCritic,
    tool_eval,
)
from arcade_tdk import ToolCatalog

import foundaudio
from foundaudio.tools.hello import say_hello

# Evaluation rubric for hello tool
rubric = EvalRubric(
    fail_threshold=0.9,  # Higher threshold for simple greeting tool
    warn_threshold=0.95,
)

# Create a catalog of tools to include in the evaluation
catalog = ToolCatalog()
catalog.add_module(foundaudio)


@tool_eval()
def hello_eval_suite() -> EvalSuite:
    """Create an evaluation suite for the hello tool.

    This evaluation suite tests the say_hello tool with various scenarios
    including simple greetings, contextual greetings, and name extraction
    from conversation history.
    """
    suite = EvalSuite(
        name="Hello Tool Evaluation Suite",
        system_message=(
            "You are an AI assistant with access to a greeting tool. "
            "Use the say_hello tool to greet users when requested."
        ),
        catalog=catalog,
        rubric=rubric,
    )

    # =============================================================================
    # BASIC GREETING EVALUATIONS
    # =============================================================================

    suite.add_case(
        name="Simple Greeting",
        user_message="Say hello to Alice",
        expected_tool_calls=[
            ExpectedToolCall(
                func=say_hello,
                args={"name": "Alice"},
            )
        ],
        critics=[
            BinaryCritic(critic_field="name", weight=1.0),
        ],
    )

    suite.add_case(
        name="Greeting with Different Name",
        user_message="Say hello to Bob",
        expected_tool_calls=[
            ExpectedToolCall(
                func=say_hello,
                args={"name": "Bob"},
            )
        ],
        critics=[
            BinaryCritic(critic_field="name", weight=1.0),
        ],
    )

    suite.add_case(
        name="Greeting with Formal Name",
        user_message="Please greet Dr. Smith",
        expected_tool_calls=[
            ExpectedToolCall(
                func=say_hello,
                args={"name": "Dr. Smith"},
            )
        ],
        critics=[
            SimilarityCritic(critic_field="name", weight=1.0),
        ],
    )

    # =============================================================================
    # CONTEXTUAL GREETING EVALUATIONS
    # =============================================================================

    suite.add_case(
        name="Contextual Greeting with Conversation History",
        user_message="He's actually right here, say hi to him!",
        expected_tool_calls=[
            ExpectedToolCall(
                func=say_hello,
                args={"name": "John Doe"},
            )
        ],
        critics=[
            SimilarityCritic(critic_field="name", weight=1.0),
        ],
        additional_messages=[
            {"role": "user", "content": "My friend's name is John Doe."},
            {
                "role": "assistant",
                "content": "It is great that you have a friend named John Doe!",
            },
        ],
    )

    suite.add_case(
        name="Greeting with Multiple People Context",
        user_message="Say hello to the person I mentioned earlier",
        expected_tool_calls=[
            ExpectedToolCall(
                func=say_hello,
                args={"name": "Sarah"},
            )
        ],
        critics=[
            SimilarityCritic(critic_field="name", weight=1.0),
        ],
        additional_messages=[
            {
                "role": "user",
                "content": "I have a colleague named Sarah who works in marketing.",
            },
            {
                "role": "assistant",
                "content": "That's interesting! What does Sarah do in marketing?",
            },
        ],
    )

    suite.add_case(
        name="Greeting with Family Context",
        user_message="Can you greet my sister?",
        expected_tool_calls=[
            ExpectedToolCall(
                func=say_hello,
                args={"name": "Emma"},
            )
        ],
        critics=[
            SimilarityCritic(critic_field="name", weight=1.0),
        ],
        additional_messages=[
            {"role": "user", "content": "My sister Emma is visiting this weekend."},
            {
                "role": "assistant",
                "content": "That sounds wonderful! I hope you have a great time with Emma.",
            },
        ],
    )

    # =============================================================================
    # EDGE CASE EVALUATIONS
    # =============================================================================

    suite.add_case(
        name="Greeting with Special Characters",
        user_message="Say hello to José-María",
        expected_tool_calls=[
            ExpectedToolCall(
                func=say_hello,
                args={"name": "José-María"},
            )
        ],
        critics=[
            BinaryCritic(critic_field="name", weight=1.0),
        ],
    )

    suite.add_case(
        name="Greeting with Numbers in Name",
        user_message="Say hello to Agent 007",
        expected_tool_calls=[
            ExpectedToolCall(
                func=say_hello,
                args={"name": "Agent 007"},
            )
        ],
        critics=[
            BinaryCritic(critic_field="name", weight=1.0),
        ],
    )

    # =============================================================================
    # CONVERSATION FLOW EVALUATIONS
    # =============================================================================

    suite.add_case(
        name="Greeting in Multi-turn Conversation",
        user_message="Now say hello to them",
        expected_tool_calls=[
            ExpectedToolCall(
                func=say_hello,
                args={"name": "Alex"},
            )
        ],
        critics=[
            SimilarityCritic(critic_field="name", weight=1.0),
        ],
        additional_messages=[
            {"role": "user", "content": "I have a friend named Alex"},
            {"role": "assistant", "content": "Nice to meet Alex! What does Alex do?"},
            {"role": "user", "content": "Alex is a software engineer"},
        ],
    )

    suite.add_case(
        name="Greeting with Implicit Request",
        user_message="I'd like you to greet my boss",
        expected_tool_calls=[
            ExpectedToolCall(
                func=say_hello,
                args={"name": "Mr. Johnson"},
            )
        ],
        critics=[
            SimilarityCritic(critic_field="name", weight=1.0),
        ],
        additional_messages=[
            {"role": "user", "content": "My boss Mr. Johnson is in the meeting room"},
            {
                "role": "assistant",
                "content": "I see, is there something specific you need to discuss with Mr. Johnson?",
            },
        ],
    )

    return suite
