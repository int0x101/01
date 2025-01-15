import pytest
from parser import parser


def test_declare():
    data = "int a"
    results = parser.parse(data)
    assert results == [("declare", "int", "a")]


def test_assign():
    data = "a = 0"
    results = parser.parse(data)
    assert results == [("assign", "a", "=", ("integer", "0"))]


def test_declare_assign():
    data = 'str a = "a"'
    results = parser.parse(data)
    assert results == [("declare_assign", "str", "a", ("string", "a"))]


def test_binop():
    data = "a = 2 + 5"
    results = parser.parse(data)
    assert results == [
        ("assign", "a", "=", ("binop", "+", ("integer", "2"), ("integer", "5")))
    ]


def test_conop():
    data = "a = b ? 1 ! 0"
    results = parser.parse(data)
    assert results == [
        (
            "assign",
            "a",
            "=",
            ("conop", ("id", "b"), ("integer", "1"), ("integer", "0")),
        )
    ]


def test_func_declare():
    data = "int[] a():\n  int b"
    results = parser.parse(data)
    assert results == [
        ("func_declare", ("array", "int"), "a", [], [("declare", "int", "b")])
    ]
