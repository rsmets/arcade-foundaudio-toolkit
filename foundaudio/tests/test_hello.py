import pytest
from arcade_tdk.errors import ToolExecutionError

from foundaudio.tools.hello import say_hello


def test_hello() -> None:
    result = say_hello("developer")
    if result != "Hello, developer!":
        raise AssertionError(f"Expected 'Hello, developer!', got '{result}'")


def test_hello_raises_error() -> None:
    with pytest.raises(ToolExecutionError):
        say_hello(1)
