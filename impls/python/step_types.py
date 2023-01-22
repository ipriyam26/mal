class MalExceptions(Exception):
    def __init__(self, message):
        self.message = message

#keyword
def _keyword(string):
    return '\u029e' + string if string[0] != '\u029e' else string
    
#check if its a keyword
def _keyword_check(string):
    return  type(string) ==str and len(string)!=0 and string[0] == '\u029e' 

class List:
    def __add__(self, other):
        return List(self.list.__add__(other.list))