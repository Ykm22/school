import sys
from Gramatica import Gramatica

if __name__ == "__main__":
    gramatica = Gramatica(sys.argv[1])
    gramatica.print_right_recursive_productions()