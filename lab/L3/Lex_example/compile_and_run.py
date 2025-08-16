import subprocess

TEST_FILE = "f.txt"

def run_command(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return e.output, e.stderr

# Run Lex command
lex_command = ["lex", "-o", "scanner.c", "scanner.l"]
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
gcc_command = ["gcc", "scanner.c", "-o", "scanner.exe"]
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

# Run scanner.exe
scanner_command = ["./scanner.exe", TEST_FILE]
scanner_stdout, scanner_stderr = run_command(scanner_command)

# Print scanner.exe output
print("\nScanner output:")
print(scanner_stdout)

# Print scanner.exe errors
if scanner_stderr:
    print("Scanner errors:")
    print(scanner_stderr)

# Check for scanner.exe errors
if "error" in scanner_stderr.lower():
    print("Scanner encountered errors.")
else:
    print("Execution completed successfully.")
