"""Basic tests for the core module."""

from CSE583_humanSayMonkeyDo.core import say_hello


def test_say_hello_returns_greeting():
    assert say_hello("World") == "Hello, World!"