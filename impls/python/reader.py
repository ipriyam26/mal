import re
from mal_types import _list, _vector, _hash_map, _keyword, _symbol, _u


class Reader:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.position = 0

    def next(self):
        if self.position >= len(self.tokens):
            return None
        self.position += 1
        return self.tokens[self.position - 1]

    def peek(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None


def read_str(string: str):

    reader = Reader(tokenize(string))
    if reader.tokens == []:
        raise SyntaxError("EOF")
    # return
    return read_form(reader)


def tokenize(string: str):

    tre = re.compile(
        r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:[\\].|[^\\"])*"?|;.*|[^\s\[\]{}()'"`@,;]+)"""
    )
    return [t for t in re.findall(tre, string) if t[0] != ";"]


def read_atom(reader: Reader):
    int_regex = re.compile(r"-?[0-9]+$")
    float_regex = re.compile(r"-?[0-9]+\.[0-9]+$")
    string_regex = re.compile(r'"(?:[\\].|[^\\"])*"')
    token = reader.next()
    if int_regex.match(token):
        return int(token)
    elif float_regex.match(token):
        return float(token)
    elif string_regex.match(token):
        return escape_string(token[1:-1])

    elif token[0] == ":":
        return _keyword(token[1:])
    elif token[0] == '"':
        raise SyntaxError("unbalanced '\"'")
    elif token == "nil":
        return None
    elif token == "true":
        return True
    elif token == "false":
        return False
    else:
        return _symbol(token)


def escape_string(string: str):
    return (
        string.replace("\\\\", _u("\u029e"))
        .replace('\\"', '"')
        .replace("\\n", "\n")
        # .replace('\\\\')
        .replace(_u("\u029e"), "\\")
    )


def read_sequence(
    reader: Reader,
    data_type=list,
    start: str = "(",
    end: str = ")",
):
    abstract_syntax_tree = data_type()
    token = reader.next()
    if token != start:
        raise SyntaxError(f"expected '{start}' but got {token}")
    # is not lets look at the next character
    token = reader.peek()
    while token != end:
        if not token:
            raise SyntaxError(f"expected '{end}', got EOF")
        abstract_syntax_tree.append(read_form(reader))
        token = reader.peek()
    reader.next()
    return abstract_syntax_tree


def read_hash_map(reader):
    lst = read_sequence(reader, list, "{", "}")
    return _hash_map(*lst)


def read_list(reader):
    return read_sequence(reader, _list, "(", ")")


def read_vector(reader):
    return read_sequence(reader, _vector, "[", "]")


def read_form(reader):
    token = reader.peek()
    # reader macros/transforms
    if token[0] == ";":
        reader.next()
        return None
    elif token == "'":
        reader.next()
        return _list(_symbol("quote"), read_form(reader))
    elif token == "`":
        reader.next()
        return _list(_symbol("quasiquote"), read_form(reader))
    elif token == "~":
        reader.next()
        return _list(_symbol("unquote"), read_form(reader))
    elif token == "~@":
        reader.next()
        return _list(_symbol("splice-unquote"), read_form(reader))
    elif token == "^":
        reader.next()
        meta = read_form(reader)
        return _list(_symbol("with-meta"), read_form(reader), meta)
    elif token == "@":
        reader.next()
        return _list(_symbol("deref"), read_form(reader))

    # list
    elif token == ")":
        raise SyntaxError("unexpected ')'")
    elif token == "(":
        return read_list(reader)

    # vector
    elif token == "]":
        raise SyntaxError("unexpected ']'")
    elif token == "[":
        return read_vector(reader)

    # hash-map
    elif token == "}":
        raise SyntaxError("unexpected '}'")
    elif token == "{":
        return read_hash_map(reader)

    # atom
    else:
        return read_atom(reader)
