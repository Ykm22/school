class SymbolTable:
    def __init__(self):
        self.size = 100
        self.symbols = [None] * self.size
    
    def hash_function(self, name):
        total = sum(ord(char) for char in name)
        return total % self.size
    
    def insert(self, name, value):
        name = str(name)
        index = self.hash_function(name)
        if self.symbols[index] is None:
            self.symbols[index] = []
        if (name, value) not in self.symbols[index]:
            self.symbols[index].append((name, value))
        return index

    def find(self, name):
        name = str(name)
        index = self.hash_function(name)
        if self.symbols[index]:
            for entry in self.symbols[index]:
                if entry[0] == name:
                    return entry[1]
        return None
    
    def remove(self, name):
        name = str(name)
        index = self.hash_function(name)
        if self.symbols[index]:
            for entry in self.symbols[index]:
                if entry[0] == name:
                    self.symbols[index].remove(entry)
                    return
        return "Symbol not found"

    def print(self):
        for index in range(self.size):
            if self.symbols[index]:
                for entry in self.symbols[index]:
                    print(f"atom = {entry[0]} ---- cod_ts = {index}")


    