class Env:
    def __init__(self,outer=None,binds=None,exprs=None) -> None:
        self.data ={}
        self.outer = outer
        if binds:
            for i in range(len(binds)):
                if binds[i] == "&":
                    self.data[binds[i+1]] = exprs[i:]
                    break
                self.data[binds[i]] = exprs[i]
    
        
    def set(self,key,value):
        self.data[key]=value
        return value
        
    def find(self,key):
        if key in self.data:
            return self
        else:
            return None if self.outer is None else self.outer.find(key)
        
    def get(self,key):
        result = self.find(key)
        if result is None:
            raise Exception(f"{key} not found")
        return result.data[key]
        
        
        