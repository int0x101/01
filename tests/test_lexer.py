import pytest
from lexer import lexer


def test_token():
    data = "\n"
    lexer.input(data)
    tokens = list(lexer)
    tokens