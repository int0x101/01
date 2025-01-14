import re
import ply.lex as lex

keywords = {
    "bool": "BOOL",
    "int": "INT",
    "double": "DOUBLE",
    "str": "STRING",
    "enum": "ENUM",

    "return": "RETURN",
    "when": "WHEN",
    "else": "ELSE",
    "pass": "PASS",
    "class": "CLASS",
    "void": "VOID",
}

tokens = (
    "INDENT",
    "DEDENT",
    "NEWLINE",
    "DOUBLEL",
    "STRING",
    "INTEGER",
    "BOOLEAN",
    "ID",

    "EQUAL",
    "EQ",
    "NEQ",
    "LT",
    "GT",
    "LTE",
    "GTE",
    "LPAR",
    "RPAR",
    "LBRACE",
    "RBRACE",
    "LBRACKET",
    "RBRACKET",
    "DOT",
    "COMMA",
    "SLASH",
    "STAR",
    "COLON"
) + tuple(keywords.values())

t_EQUAL = r"="

t_EQ = r"=="
t_NEQ = r"!="
t_LT = r"<"
t_GT = r">"
t_LTE = r"<="
t_GTE = r">="

t_LPAR = r"\("
t_RPAR = r"\)"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_DOT = r"\."
t_COMMA = r","
t_SLASH = r"/"
t_STAR = r"\*"
t_COLON = r":"

indentation_stack = [0]

def t_NEWLINE(t):
    r"\n+"
    t.lexer.lineno += len(t.value)
    t.lexer.linestart = t.lexer.lexpos
    return t

def t_DOUBLEL(t):
    r"\d+\.\d+"
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t


def t_INTEGER(t):
    r"\d+"
    return t

def t_BOOLEAN(t):
    r"true|false"
    return t

def t_ID(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    t.type = keywords.get(t.value, "ID")
    return t

def t_whitespaces(t):
    r"(?<=\n)[ \t]+"
    t.value = len(t.value) - 1
    if t.value > indentation_stack[-1]:
        indentation_stack.append(t.value)
        t.type = "INDENT"
        return t
    elif t.value < indentation_stack[-1]:
        while indentation_stack[-1] > t.value and len(indentation_stack) > 1:
            t.lexer.lexpos -= 1
            t.value = indentation_stack[-1]
            indentation_stack.pop()
            t.type = "DEDENT"
        return t
    return None

def t_skip(t):
    r"[ \t]+"
    pass


def t_error(t):
    raise Exception(
        "Illegal character '%s' on line %d, column %d"
        % (t.value[0], t.lexer.lineno, t.lexer.lexpos - t.lexer.linestart + 1)
    )

def sanitize(data):
    multiple_newlines_regex = r"\n+"
    sanitized_newline = "\n "
    return re.sub(multiple_newlines_regex, sanitized_newline, data.lstrip())


lexer = lex.lex()
input_function = lexer.input
lexer.input = lambda data: input_function(sanitize(data))
