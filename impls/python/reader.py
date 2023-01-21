import re
class Reader:
    def __init__(self, objects:list):
        self.objects = objects
    
    def next(self):
        pass

    def peek(self):
        pass

def read_str(string:str):
    pass

def tokenize(string:str):
    return re.findall("[\s,]*(~@|[\[\]{}()'`~^@]|\"(?:\\.|[^\\\"])*\"?|;.*|[^\s\[\]{}('\"`,;)]*)",string)