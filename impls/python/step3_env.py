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
from env import Env
import reader
import printer


history_list = []


def read() -> str:
    return reader.read_str(input())


def eval_ast(ast, repl_env: dict):
    if _is_symbol(ast):
        repl_env.get(ast)
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
        if ast[0] == "def!":
            return repl_env.set(ast[1], eval(ast[2], repl_env))
        elif ast[0] == "let*":
            let_env = Env(outer=repl_env)
            for i in range(0, len(ast[1]), 2):
                let_env.set(ast[1][i], eval(ast[1][i + 1], let_env))
            return eval(ast[2], let_env)
        else:
            result = eval_ast(ast, repl_env)
            return result[0](*result[1:])

        # elif _is_list(ast):
        #     result = eval_ast(ast=ast, repl_env=repl_env)
        #     return result[0](result[1], result[2])

    return ast


def print_call(character):
    print(printer.pr_str(character, print_readably=True))


def repl():
    repl_env = Env()
    res = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: int(a / b),
    }
    for key, value in res.items():
        repl_env.set(key, value)

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
