import re
import ply.lex as lex

keywords = {}

tokens = (
    "INDENT",
    "DEDENT",
    "NEWLINE",
) + tuple(keywords.values())

indentation_stack = [0]

def t_NEWLINE(t):
    r"\n+"
    t.lexer.lineno += len(t.value)
    t.lexer.linestart = t.lexer.lexpos
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
