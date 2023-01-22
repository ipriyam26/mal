class MalExceptions(Exception):
    def __init__(self, message):
        self.message = message


# keyword
def _keyword(string):
    return "\u029e" + string if string[0] != "\u029e" else string


# check if its a keyword
def _keyword_check(string):
    return type(string) == str and len(string) != 0 and string[0] == "\u029e"


class List(list):
    def __add__(self, other):
        return List(self.list.__add__(other.list))

    def __getitem__(self, key):
        return self.list[key] if key < len(self) else None

    def __getslice__(self, *a):
        return List(self.__getslice__(self, *a))


def _list(*vals):
    return List(vals)


def _list_check(exp):
    return type(exp) == List


# vectors
class Vector(list):
    def __add__(self, rhs):
        return Vector(list.__add__(self, rhs))

    def __getitem__(self, i):
        if type(i) == slice:
            return Vector(list.__getitem__(self, i))
        elif i >= len(self):
            return None
        else:
            return list.__getitem__(self, i)

    def __getslice__(self, *a):
        return Vector(list.__getslice__(self, *a))


def _vector(*vals):
    return Vector(vals)


def _vector_check(exp):
    return type(exp) == Vector


class HashMap(dict):
    pass


def _hash_map(*args):
    if len(args) % 2 != 0:
        raise MalExceptions("odd number of arguments")
    hm = HashMap()
    for i in range(0, len(args), 2):
        hm[args[i]] = args[i + 1]
    return hm


def _hash_map_check(exp):
    return type(exp) == HashMap


# atoms
class Atom(object):
    def __init__(self, val):
        self.val = val


def _atom(val):
    return Atom(val)


def _atom_Q(exp):
    return type(exp) == Atom


def py_to_mal(obj):
    if type(obj) == list:
        return List(obj)
    if type(obj) == tuple:
        return List(obj)
    elif type(obj) == dict:
        return HashMap(obj)
    else:
        return
