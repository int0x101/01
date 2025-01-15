import pytest
from lexer import lexer


def test_token():
    data = "a = a ? 1 ! 0"
    lexer.input(data)
    tokens = list(lexer)
    # print(tokens)
