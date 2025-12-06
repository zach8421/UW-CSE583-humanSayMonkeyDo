"""Basic tests for the core module."""

from cse583_human_say_monkey_do.core import say_hello


def test_say_hello_returns_greeting():
    assert say_hello("World") == "Hello, World!"