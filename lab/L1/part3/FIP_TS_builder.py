import os
import argparse
from SymbolTable import SymbolTable

# py .\FIP_TS_builder.py ..\atoms\l1_p1.cpp.txt .\atom_codes.txt

def read_cmd_line():
    parser = argparse.ArgumentParser(description="CLA parser")
    parser.add_argument('atoms_file')
    parser.add_argument('atom_codes_file')
    args = parser.parse_args()
    return args.atoms_file, args.atom_codes_file

def read_atoms(atoms_file):
    atoms = []
    try:
        with open(atoms_file, 'r') as file:
            for line in file:
                if line[0] == ",":
                    # atoms[","] = "separator"
                    atoms.append((",", "separator"))
                else:
                    line = line.strip().split(',')
                    # atoms[line[0]] = line[1]
                    atoms.append((line[0], line[1]))
    except FileNotFoundError:
        print("The file does not exist.")
    except Exception as e:
        print(f"Erorr: {e}")
    return atoms

def read_atom_codes(atom_codes_file):
    atom_codes = {}
    try:
        with open(atom_codes_file, 'r') as file:
            for line in file:
                if line[0] == ",":
                    line = line.strip().split(',')
                    # atom_codes.append((",", line[:-1]))
                    atom_codes[","] = line[-1]
                else:
                    line = line.strip().split(',')
                    # atom_codes.append((line[0], line[1]))
                    atom_codes[line[0]] = line[1]
    except FileNotFoundError:
        print("The file does not exist.")
    except Exception as e:
        print(f"Erorr: {e}")
    return atom_codes

def build_symbol_tables(idSymbolTable, constSymbolTable, atoms, atom_codes):
    for atom, type in atoms:
        if type == "ID":
            index = idSymbolTable.insert(atom, " ")
        elif type == "CONST":
            index = constSymbolTable.insert(atom, " ")
        else:
            index = "-"
        if type == "separator" or type == "operator":
            type = atom
        print(f"atom = {atom}  ----  cod atom = {atom_codes[type]}  ----  cod_ts = {index}")    

if __name__ == "__main__":
    atoms_file, atom_codes_file = read_cmd_line()
    atoms = read_atoms(atoms_file)
    atom_codes = read_atom_codes(atom_codes_file)

    idSymbolTable = SymbolTable()
    constSymbolTable = SymbolTable()
    print("FIP")
    build_symbol_tables(idSymbolTable, constSymbolTable, atoms, atom_codes)
    print("\nID symbol table")
    idSymbolTable.print()
    print("\nCONST symbol table")
    constSymbolTable.print()
    
