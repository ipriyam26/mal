import sys
from core import ns
import traceback
from mal_types import (
    _is_symbol,
    _is_list,
    _is_vector,
    _hash_is_map,
    _vector,
    _hash_map,
    HashMap,
    _function,
    _symbol,
)
from env import Env
import reader
import printer


history_list = []


def read(str_input) -> str:
    
    return reader.read_str(str_input)


def eval_ast(ast, repl_env: dict):
    if _is_symbol(ast):
        return repl_env.get(ast)
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


def eval(ast, repl_env: Env) -> str:
    if ast == "history":
        ast = history(True)
    else:
        history(character=ast)
        if not _is_list(ast):
            return eval_ast(ast, repl_env)
        elif len(ast) == 0:
            return ast
        if ast[0] == "def!":
            res = eval(ast[2], repl_env)
            return repl_env.set(ast[1], res)
        elif ast[0] == "let*":
            let_env = Env(outer=repl_env)
            for i in range(0, len(ast[1]), 2):
                let_env.set(ast[1][i], eval(ast[1][i + 1], let_env))
            ast = ast[2]
            repl_env = let_env
        elif ast[0] == "do":
            eval_ast(ast[1:-1], repl_env)
            ast = ast[-1]
        elif ast[0] == "if":
            res = eval(ast[1], repl_env)
            if res is not None and res is not False:
                ast = ast[2]

            elif len(ast) <= 3:
                ast = None
            else:
                ast = ast[3]
                
        elif ast[0] == "fn*":
            return _function(eval, Env, ast[2], repl_env, ast[1])
        else:
            result = eval_ast(ast, repl_env)
            fnc = result[0]
            if hasattr(fnc, "__ast__"):
                ast = fnc.__ast__ 
                repl_env = fnc.__gen_env__(result[1:])
            else:
                return fnc(*result[1:])
                


def print_call(character):
    print(printer.pr_str(character, print_readably=True))


def repl(str_input:str):

    character = read(str_input)
    character = eval(character, repl_env)
    print_call(character=character)


def history(output: bool = False, character: str = None):
    if output:
        return "\n".join(history_list)
    else:
        history_list.append(character)


repl_env = Env()


for key, value in ns.items():
    repl_env.set(_symbol(key), value)

repl("(def! not (fn* (a) (if a false true)))")

while True:
    try:
        print("user> ", end="")
        str_input = input()
        # if str_input == "exit":
        #     break
        # if str_input == "":
        #     continue
        
        repl(str_input=str_input)
    except Exception as e:
        print("".join(traceback.format_exception(*sys.exc_info())))
