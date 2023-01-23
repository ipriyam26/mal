class Env:
    def __init__(self,outer=None) -> None:
        self.data ={}
        self.outer = outer
        
    def set(self,key,value):
        self.data[key]=value
        
    def find(self,key):
        if key in self.data:
            return self
        else:
            return None if self.outer is None else self.outer.find(key)
        
    def get(self,key):
        result = self.find(key)
        if result is None:
            raise SyntaxError("Not found", key)
        return result.data[key]
        