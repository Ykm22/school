# commands shortcuts
# py .\atom_identifier.py .\l1_p1\l1_p1.cpp
# py .\atom_identifier.py .\l1_p2\l1_p2.cpp
# py .\atom_identifier.py .\l1_p3\l1_p3.cpp
# py .\atom_identifier.py .\l1_p4\l1_p4.cpp


import os
import argparse
from AF import AF

def read_cmd_line():
    parser = argparse.ArgumentParser(description="CLA parser")
    parser.add_argument('input_file')
    args = parser.parse_args()
    return args.input_file

punctuationMarks = [";", ",", " ", "(", ")", "{", "}", "", ">", "<"]
def isPunctuatonMark(ch):
    if(ch in punctuationMarks):
        return True
    return False

def endsInPunctuationMark(atom):
    if(isPunctuatonMark(atom[-1])):
        return True
    return False

def beginsWithPunctuationMark(atom):
    if(isPunctuatonMark(atom[0])):
        return True
    return False 

def clean_atom(atom):
    # if(isPunctuatonMark(atom)):
    #     return None
    # while endsInPunctuationMark(atom):
    #     atom = atom[0:-1]
    # while beginsWithPunctuationMark(atom):
    #     atom = atom[1:]
    if atom == "":
        return None
    return atom

def isInteger(atom):
    return atom.isdigit() or (atom[0] == '-' and atom[1:].isdigit())

def isFloat(atom):
    try:
        float(atom)
        return True
    except Exception:
        return False

def isOperator(atom):
    operators = ["+", "-", "/", "%", "=", "<<", ">>", "!=", "*"]
    return atom in operators

def isIdentifier(atom):
    return atom.isalpha()

def isKeyword(atom):
    keywords = ["while", "if", "for", "int", "float", "namespace", "using", "include", "return", "else", "std", "iostream", "double"]
    return atom in keywords or ( atom[0] == '<' and atom[-1] == '>')

def isHexa(atom):
    return atom[0] == "0" and atom[1] == "x" and isInteger(atom[2:])

def isSeparator(atom):
    return atom == "," or atom == ";" or atom == "(" or atom == ")" or atom == "{" or atom == "}"

def isKeywordPart(atom):
    return atom == "#" or atom == "<" or atom == ">"


def isBinary(atom):
    if atom[0] == "0" and atom[1] == "b":
        for i in range(2, len(atom)):
            if atom[i] != "0" and atom[i] != "1":
                return False
        return True
    return False

def save_atoms(atoms, output_file):
    for atom in atoms:
        if atom != None:
            output_file.write(atom + ",")
            if isInteger(atom):
                output_file.write("int")
            elif isFloat(atom):
                output_file.write("float")
            elif isHexa(atom):
                output_file.write("hexa")
            elif isBinary(atom):
                output_file.write("binary")
            elif isOperator(atom):
                output_file.write("operator")
            elif isKeyword(atom):
                output_file.write("keyword")
            elif isSeparator(atom):
                output_file.write("separator")
            elif isIdentifier(atom):
                output_file.write("ID")
            else:
                output_file.write("unknown symbol\n")
                quit()
            output_file.write("\n")

def save_atoms_v2(atoms, output_file):
    for atom, type in atoms:
        output_file.write(atom + ",")
        if type == "ID":
            if isKeyword(atom):
                output_file.write("keyword")
            else:
                output_file.write("ID")
        elif type == "CONST":
            output_file.write("CONST")
        elif type == "operator":
            output_file.write("operator")
        elif type == "separator":
            output_file.write("separator")
        else:
            print(type)
            output_file.write("unknown symbol\n")
            quit()
        output_file.write("\n")

def delete_output_file(file, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    if os.path.exists(file):
        os.remove(file)

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


def load_AF(file_name):
    with open(file_name, "r") as file:
        alphabet, transitions_alphabet, final_states, initial_state, transitions = read_data(file)
        af = AF(alphabet, transitions_alphabet, final_states, initial_state, transitions)
        return af

def main(input_file):
    import string
    LETTERS = (
        string.ascii_lowercase + string.ascii_uppercase
    )

    NUMBERS = "0123456789"

    AF_IDS = load_AF("AF_IDS.txt")
    AF_INTS = load_AF("AF_INTS.txt")
    AF_FLOATS = load_AF("AF_FLOATS.txt")
    
    # print()
    # AF_FLOATS.print_transitions()
    # print()

    # print(AF_FLOATS.longest_prefix("3"))
    # print(AF_INTS.longest_prefix("3"))

    try:
        with open(input_file, 'r') as file:
            directory = "atoms"
            output_file = os.path.join(directory, (file.name).split('\\')[-1] + ".txt")
            delete_output_file(output_file, directory)

            with open(output_file, 'w') as output_file:
                curr_atom = ""
                # type
                # 0 - illegal
                # 1 - identifier
                # 2 - number
                type = 0 
                atoms = []

                while True:
                    ids_result = None
                    ch = file.read(1)
                    
                    curr_atom += ch
                    if curr_atom == "":
                        pass

                    elif (type == 0 and ch in LETTERS) or type == 1:
                        type = 1
                        ids_result = AF_IDS.longest_prefix(curr_atom)

                        if len(ids_result) != len(curr_atom):
                            if isKeyword(curr_atom): 
                                atoms.append((curr_atom, "ID"))
                                curr_atom = ""
                                type = 0
                            else:
                                if not isSeparator(ch) and not isPunctuatonMark(ch) and not isOperator(ch):
                                    print(f"Incorrect file, found: {curr_atom}")
                                    exit(1)
                                atoms.append((ids_result, "ID"))
                                curr_atom = ""
                                type = 0

                    elif (type == 0 and ch in NUMBERS) or type == 2:
                        type = 2
                        int_result = AF_INTS.longest_prefix(curr_atom)

                        if ch == ".":
                            type = 3
                        else:
                            if len(int_result) != len(curr_atom):
                                if not isSeparator(ch) and not isPunctuatonMark(ch) and not isOperator(ch):
                                    print(f"Incorrect file, found: {curr_atom}")
                                    exit(1)

                                atoms.append((int_result, "CONST"))
                                curr_atom = ""
                                type = 0

                    elif type == 3:
                        float_result = AF_FLOATS.longest_prefix(curr_atom)

                        if float_result == False:
                            print(f"Incorrect file, found: {curr_atom}")
                            exit(1)

                        if len(float_result) < len(curr_atom):
                            if not isSeparator(ch) and not isPunctuatonMark(ch) and not isOperator(ch):
                                print(f"Incorrect file, found: {curr_atom}")
                                exit(1)
                            atoms.append((float_result, "CONST"))
                            curr_atom = ""
                            type = 0


                    else:
                        if not isSeparator(ch) and not isKeywordPart(ch) and ch != " " and ch != "\"" and ch != "\n":
                            print(f"curr_atom = {curr_atom}, ch = {ch} xd")
                            print("Incorrect input file")
                            exit(1)
                        curr_atom = ""
                        type = 0

                    if isSeparator(ch):
                        atoms.append((ch, "separator"))
                    elif isOperator(ch):
                        atoms.append((ch, "operator"))

                    if not ch:
                        # EOF
                        break

                save_atoms_v2(atoms, output_file)
                # L2 implementation
                # for line in file:
                    # line = line.strip().split(' ')
                    # atoms = [clean_atom(atom) for atom in line]
                    # save_atoms(atoms, output_file)
        

    except FileNotFoundError:
        print("The file does not exist.")
    except Exception as e:
        print(f"Erorr: {e}")

if __name__ == "__main__":
    input_file = read_cmd_line()
    main(input_file)
