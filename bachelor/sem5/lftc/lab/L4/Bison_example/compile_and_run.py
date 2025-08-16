import sys
import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return e.output, e.stderr

# Check if the input file is provided
if len(sys.argv) != 2:
    print("Usage: python script.py input_file")
    sys.exit(1)

input_file = sys.argv[1]

# Run Bison command
bison_command = ["bison", "-d", "analyzer.y"]
bison_stdout, bison_stderr = run_command(bison_command)

# Print Bison command output
print("Bison command output:")
print(bison_stdout)

# Print Bison command errors
if bison_stderr:
    print("Bison command errors:")
    print(bison_stderr)

# Check for Lex errors
if "error" in bison_stderr.lower():
    print("Bison command encountered errors. Exiting.")
    exit(1)

# Run Lex command
lex_command = ["flex", "analyzer.l"]
lex_stdout, lex_stderr = run_command(lex_command)

# Print Lex command output
print("Lex command output:")
print(lex_stdout)

# Print Lex command errors
if lex_stderr:
    print("Lex command errors:")
    print(lex_stderr)

# Check for Lex errors
if "error" in lex_stderr.lower():
    print("Lex command encountered errors. Exiting.")
    exit(1)

# Run GCC command
gcc_command = ["gcc", "analyzer.tab.c", "lex.yy.c", "SymbolTableCONSTS.c", "SymbolTableIDS.c", "-o", "analyzer.exe"]
gcc_stdout, gcc_stderr = run_command(gcc_command)

# Print GCC command output
print("\nGCC command output:")
print(gcc_stdout)

# Print GCC command errors
if gcc_stderr:
    print("GCC command errors:")
    print(gcc_stderr)

# Check for GCC errors
if "error" in gcc_stderr.lower():
    print("GCC command encountered errors. Exiting.")
    exit(1)

# Run analyzer.exe with the input file as an argument
analyzer_command = ["./analyzer.exe", input_file]
analyzer_stdout, analyzer_stderr = run_command(analyzer_command)

# Print analyzer.exe output
print("\nAnalyzer output:")
print(analyzer_stdout)

# Print analyzer.exe errors
if analyzer_stderr:
    print("Analyzer errors:")
    print(analyzer_stderr)

# Check for analyzer.exe errors
if "error" in analyzer_stderr.lower():
    print("Analyzer encountered errors.")
else:
    print("Execution completed successfully.")
