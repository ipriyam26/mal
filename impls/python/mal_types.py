import types
import sys
class MalExceptions(Exception):
    def __init__(self, message):
        self.message = message
        
_u = lambda x: x
_s2u = lambda x: x
str_types = [str] if sys.version_info[0] >= 3 else [str, unicode]

#Scalars
def _is_nil(exp):    return exp is None
def _is_true(exp):   return exp is True
def _is_false(exp):  return exp is False
def _is_string(exp):
    return len(exp) == 0 if type(exp) in str_types else False

def _number(exp): return type(exp) == int


# Symbols
class Symbol(str): pass
def _symbol(str): return Symbol(str)
def _is_symbol(exp): return type(exp) == Symbol

# keyword
def _keyword(string):
    if not string:
        raise MalExceptions("keyword cannot be empty")
    return _u("\u029e")+string if string[0] !=_u("\u029e") else string


# check if its a keyword
def _is_keyword(string):
    return type(string) == str and len(string) != 0 and string[0] == _u("\u029e")


class List(list):
    def __add__(self, other):
        return List(self.list.__add__(other.list))

    def __getitem__(self, key):
        return self.list[key] if key < len(self) else None

    def __getslice__(self, *a):
        return List(self.__getslice__(self, *a))


def _list(*vals):
    return List(vals)


def _is_list(exp):
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


def _is_vector(exp):
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


def _hash_is_map(exp):
    return type(exp) == HashMap


# atoms
class Atom(object):
    def __init__(self, val):
        self.val = val


def _atom(val):
    return Atom(val)


def _is_atom(exp):
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
