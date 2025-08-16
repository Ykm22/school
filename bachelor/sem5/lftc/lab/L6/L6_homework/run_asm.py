import subprocess

def run_commands(asm_filename):
    # Assemble the assembly code
    assemble_command = f'nasm -f win32 {asm_filename}.asm'
    subprocess.run(assemble_command, shell=True, check=True)

    # Link the object file
    link_command = f'./nlink.exe {asm_filename}.obj -lio -o {asm_filename}.exe'
    subprocess.run(link_command, shell=True, check=True)

    # Run the executable
    run_command = f'./{asm_filename}.exe'
    subprocess.run(run_command, shell=True, check=True)

if __name__ == "__main__":
    asm_filename = input("Enter the ASM file name (without extension): ")
    run_commands(asm_filename)