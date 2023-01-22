import re


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
    # [\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"?|;.*|[^\s\[\]{}('"`,;)]*)
    tre = re.compile(
        r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:[\\].|[^\\"])*"?|;.*|[^\s\[\]{}()'"`@,;]+)"""
    )
    return [t for t in re.findall(tre, string) if t[0] != ";"]


def read_list(reader: Reader):
    current_tokens = []
    reader.next()
    # if it reaches EOF before closing the list it should throw an error
    while reader.peek() != ")":
        current_tokens.append(read_form(reader))
        # reader.next()
    reader.next()
    return current_tokens


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
    elif token[0] == '"':
        raise SyntaxError("unbalanced '\"'")
    elif token == "nil":
        return None
    elif token == "true":
        return True
    elif token == "false":
        return False
    else:
        return token


def escape_string(string: str):
    return (
        string.replace("\\\\", "\u029e")
        .replace('\\"', '"')
        .replace("\\n", "\n")
        # .replace('\\\\')
        .replace("\u029e", "\\")
    )


def read_form(reader: Reader):
    token = reader.peek()
    if token == "(":
        # reader.next()
        return read_list(reader)
    elif token == ")":
        raise SyntaxError("unexpected ')'")
    else:
        return read_atom(reader)
