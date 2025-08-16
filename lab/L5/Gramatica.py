import string

class Gramatica():
    def __init__(self, file_path):
        self.terminals = set()
        self.non_terminals = set()
        self.productions = {}

        with open(file_path, "r") as file:
            for line in file:
                left_side, right_side = line.strip().split("->")
                
                if not left_side in self.productions.keys():
                    self.productions[left_side] = []

                self.terminals.add(left_side)

                right_side_arr = []

                for letter in right_side:
                    right_side_arr.append(letter)
                    if letter in string.ascii_lowercase:
                        self.non_terminals.add(letter)
                self.productions[left_side].append(right_side_arr)

    def print(self):
        print(self.terminals)
        print(self.non_terminals)
        print(self.productions)

    def print_right_recursive_productions(self):
        for key in self.productions.keys():
            productions = self.productions[key]
            for production in productions:
                if key == production[-1]:
                    print(f"{key} -> {production}")