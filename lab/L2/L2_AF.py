from AF import AF
import sys

'''
File input: AF1.txt, AF2.txt
Console input: copy from file input and paste into console, add new line with CTRL+Z before enter
'''

def handle_console_input():
    lines = []
    while True:
        user_input = sys.stdin.readline()
        if not user_input:
            break
        lines.append(user_input.strip())

    alphabet, transitions_alphabet, final_states, initial_state, transitions = read_data(lines)
    af = AF(alphabet, transitions_alphabet, final_states, initial_state, transitions)
    return af

def read_alphabet(line : str):
    alphabet_line = line.strip().split("=")[1]
    states = alphabet_line.split(",")
    return states

def read_transitions_alphabet(line : str):
    transitions_alphabet = line.strip().split("=")[1]
    transitions = transitions_alphabet.split(",")
    return transitions

def read_final_states(line : str):
    final_sates_line = line.strip().split("=")[1]
    final_states = final_sates_line.split(",")
    return final_states

def read_initial_state(line : str):
    initial_state = line.strip().split("=")[1]
    return initial_state

def add_transition(line: str, transitions: dict) :
    origin_state, transition_pairs = line.strip().split(":")
    transition_pairs = transition_pairs.split(";")

    if origin_state not in transitions:
        transitions[origin_state] = []

    for pair in transition_pairs:
        pair = pair[1:-1]
        neighbor_state, transition_path = pair.split(",")
        transitions[origin_state].append((neighbor_state, transition_path))

def read_data(input_file):
    alphabet = []
    transitions_alphabet = []
    final_states = []
    initial_state = None
    transitions = {}
    for line_index, line in enumerate(input_file, start=1):
        if line_index == 1:
            alphabet = read_alphabet(line)
        if line_index == 2:
            transitions_alphabet = read_transitions_alphabet(line)
        if line_index == 3:
            final_states = read_final_states(line)
        if line_index == 4:
            initial_state = read_initial_state(line)
        if line_index > 4:
            add_transition(line, transitions)
    return alphabet, transitions_alphabet, final_states, initial_state, transitions

def handle_file_input():
    file_name = input("AF File name = ")
    with open(file_name, "r") as file:
        alphabet, transitions_alphabet, final_states, initial_state, transitions = read_data(file)
        af = AF(alphabet, transitions_alphabet, final_states, initial_state, transitions)
        return af

def read():
    print("AF va fi citit din:")
    print("1 - Consola")
    print("2 - Fisier")

    cmd = input(">>> ")
    if cmd == "1":
        af = handle_console_input()
    if cmd == "2":
        af = handle_file_input()
    return af
    
def print_commands():
    print("----------------------")
    print("Commands")
    print("1 - Multimea starilor")
    print("2 - Alfabet")
    print("3 - Tranzitii")
    print("4 - Stari finale")
    print("5 - Testare secventa")
    print("6 - Cel mai lung prefix valid")
    print("0 - Quit")

def menu(af):
    while True:
        print_commands()
        cmd = input(">>> ")
        if cmd == "0":
            quit()
        elif cmd == "1":
            af.print_states()
        elif cmd == "2":
            af.print_alphabet()
        elif cmd == "3":
            af.print_transitions()
        elif cmd == "4":
            af.print_final_states()
        elif cmd == "5":
            sequence = input("Secventa, elementele alfabetului separate prin virgula: ")
            sequence = sequence.strip().split(",")
            print(af.test_sequence(sequence))
        elif cmd == "6":
            sequence = input("Secventa, elementele alfabetului separate prin virgula: ")
            sequence = sequence.strip().split(",")
            print(af.longest_prefix(sequence))
        else:
            quit()

if __name__ == "__main__":
    af = read()
    menu(af)
