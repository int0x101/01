import pytest
from lexer import lexer


def test_newline():
    data = "\n"
    lexer.input(data)
    tokens = list(lexer)
    assert len(tokens) == 1 and tokens[0].type == "NEWLINE"


def test_indentation():
    data = "    "
    lexer.input(data)
    tokens = list(lexer)
    assert len(tokens) == 1 and tokens[0].type == "INDENT"
