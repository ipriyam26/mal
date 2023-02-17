import time
import printer
import mal_types
import reader

ns = {
    "read-string": reader.read_str,
    "slurp": lambda filename: open(filename).read(),
    "pr-str": lambda *args: " ".join(
        [printer.pr_str(arg, print_readably=True) for arg in args]
    ),
    "str": lambda *args: "".join(
        [printer.pr_str(arg, print_readably=False) for arg in args]
    ),
    "prn": lambda *args: print(
        " ".join([printer.pr_str(arg, print_readably=True) for arg in args])
    ),
    "println": lambda *args: print(
        " ".join([printer.pr_str(arg, print_readably=False) for arg in args])
    ),
    "=": lambda a, b: a == b,
    "<": lambda a, b: a < b,
    "<=": lambda a, b: a <= b,
    ">": lambda a, b: a > b,
    ">=": lambda a, b: a >= b,
"+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: int(a / b),
    "time-ms": lambda: int(time.time() * 1000),
    "list": mal_types._list,
    "list?": mal_types._is_list,
    "vector": mal_types._vector,
    "vector?": mal_types._is_vector,
    "hash-map": mal_types._hash_map,
    "map?": mal_types._hash_is_map,
    "atom": mal_types._atom,
    "atom?": mal_types._is_atom,
    "empty?": lambda a: len(a) == 0,
    "count": lambda a: 0 if mal_types._is_nil(a) else len(a),
    "deref": lambda a: a.val,
    "refer!": lambda a, b: a.set(b),
    "swap!": lambda a, b, *c: a.swap(b, *c),
    "@": lambda a: a.val,
"reset!": lambda a, b: a.reset(b),
"cons": lambda a, b: mal_types._list(a, *b),
"concat": lambda *a: mal_types._list(*[item for sublist in a for item in sublist]),
"vec": lambda a: mal_types._vector(*a),
}
