; Compile:
; nasm -f win32 iodemo.asm
; nlink iodemo.obj -lio -o iodemo.exe

%include 'io.inc'
 global main
 section .text
main:
 mov eax, perim
 call io_writestr

 call io_readint

 mov [perim], eax
 mov eax, [perim]

 call io_writeint
section .data
 perim dd 'perim = ', 0
 input_buffer resd 1 ; Reserve space for an integer