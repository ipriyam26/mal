import sys
import traceback


history_list = []
def read() -> str:
    return input()

def eval(character: str) -> str:
    if character == "history":
        character= history(True)
    else:
        history(character=character)
    return character

def print_call(character: str):
    print(character)


def repl():
        character = read()
        character = eval(character)
        print_call(character=character)

def history(output:bool=False,character:str=None):
    if output:
        return "\n".join( history_list)
    else:
        history_list.append(character)
        
while True:
    try:
        print("user> ",end="")
        repl()
    except Exception as e:
        print("".join(traceback.format_exception(*sys.exc_info())))