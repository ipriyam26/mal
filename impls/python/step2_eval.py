import sys
import traceback
from mal_types import (
    _is_symbol,
    _is_list,
    _is_vector,
    _hash_is_map,
    _vector,
    _hash_map,
    HashMap,
)
import reader
import printer


history_list = []


def read() -> str:
    return reader.read_str(input())


def eval_ast(ast, repl_env: dict):
    if _is_symbol(ast):
        if ast in repl_env:
            return repl_env[ast]
        else:
            raise SyntaxError("Unknown symbol", ast)
    elif _is_list(ast):
        return [eval(element, repl_env=repl_env) for element in ast]

    elif _is_vector(ast):
        return _vector(*[eval(element, repl_env=repl_env) for element in ast])
    elif _hash_is_map(ast):
        ast: HashMap = ast
        result = []
        for key, value in ast.items():
            result.extend([key, eval(value, repl_env=repl_env)])
        return _hash_map(*result)
    else:
        return ast


def eval(ast, repl_env: dict) -> str:
    if ast == "history":
        ast = history(True)
    else:
        history(character=ast)
        if not _is_list(ast):
            return eval_ast(ast, repl_env)
        elif len(ast) == 0:
            return ast
        elif _is_list(ast):
            result = eval_ast(ast=ast, repl_env=repl_env)
            return result[0](result[1], result[2])

    return ast


def print_call(character):
    print(printer.pr_str(character, print_readably=True))


def repl():
    repl_env = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: int(a / b),
    }
    character = read()
    character = eval(character, repl_env)
    print_call(character=character)


def history(output: bool = False, character: str = None):
    if output:
        return "\n".join(history_list)
    else:
        history_list.append(character)


while True:
    try:
        print("user> ", end="")
        repl()
    except Exception as e:
        print("".join(traceback.format_exception(*sys.exc_info())))
