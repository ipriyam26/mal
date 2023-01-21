def read() -> str:
    return input()

def eval(character: str) -> str:
    return character

def print_call(character: str):
    print(character)


def repl():
        character = read()
        character = eval(character)
        print_call(character=character)

while True:
    print("user> ",end="")
    repl()