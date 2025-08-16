; Compile:
; nasm -f win32 iodemo.asm
; nlink iodemo.obj -lio -o iodemo.exe

%include 'io.inc'
 global main
 section .text
main:
 mov eax, str_a
 call io_writestr
 call io_readint
 mov ebx, eax
section .data
 str_a dd 'A = ', 0