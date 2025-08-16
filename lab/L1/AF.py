class AF:
    def __init__(self, alphabet, transitions_alphabet, final_states, initial_state, transitions):
        self.alphabet = alphabet # list<string>
        self.transitions_alphabet = transitions_alphabet # list<string>
        self.final_states = final_states # list<string>
        self.initial_state = initial_state # string
        self.transitions = transitions # dict<string, list<tuple<string, string>>>

    def print_states(self):
        print(f"Multimea starilor = {self.alphabet}")

    def print_alphabet(self):
        print(f"Alfabet = {self.transitions_alphabet}")

    def print_transitions(self):
        print(f"transitions = {self.transitions}")

    def print_final_states(self):
        print(f"final_states = {self.final_states}")
        # print(f"initial_state = {self.initial_state}")

    def get_neighbors(self, state):
        return self.transitions[state]

    def test_sequence(self, sequence):
        current_state = self.initial_state
        for current_path in sequence:
            if current_state in self.transitions:
                neighbors = self.get_neighbors(current_state)
            else:
                return False
            chosen_neighbor = None
            for neighbor, path in neighbors:
                if current_path == path:
                    chosen_neighbor = neighbor
            current_state = chosen_neighbor
        return current_state in self.final_states
    
    def longest_prefix(self, sequence):
        longest_prefix = None
        prefix = ""

        current_state = self.initial_state

        for current_path in sequence:

            if current_state in self.transitions:
                neighbors = self.get_neighbors(current_state)
            else:
                if longest_prefix == None:
                    return False
                else:
                    return longest_prefix
            
            chosen_neighbor = None
            for neighbor, path in neighbors:
                if current_path == path:
                    chosen_neighbor = neighbor
            current_state = chosen_neighbor
            prefix += current_path

            if current_state in self.final_states:
                longest_prefix = prefix

        return longest_prefix