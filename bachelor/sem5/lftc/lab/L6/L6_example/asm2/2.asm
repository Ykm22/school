%include 'io.inc'
 global main
 section .text
main:
 ; Assign to: pi, value: 314
 mov dword [pi], 314

 ; Assign to: area, value: 400
 mov dword [area], 400

 ; Assign to: a, value: 400
 mov dword [a], 400

 ; Assign to: b, value: a + 2
 mov eax, [a]
 add eax, 2
 mov [b], eax

 ; Assign to: c, value: b / 2
 mov eax, [b]
 xor edx, edx
 mov ecx, 2
 div ecx
 mov [c], eax

 ; Assign to: d, value: a
 mov eax, [a]
 sub eax, 2
 mov [d], eax

 ; Assign to: f, value: b
 mov eax, [b]
 imul eax, 2
 mov [f], eax

 ; Read into perim
 mov eax, perim
 call io_writestr
 call io_readint
 mov [perim], eax
 mov eax, 0

 ; Read into radius
 mov eax, radius
 call io_writestr
 call io_readint
 mov [radius], eax
 mov eax, 0

 ; Write radius
 mov eax, [radius]
 call io_writeint
 mov eax, newline_str
 call io_writestr

 ; Write perim
 mov eax, [perim]
 call io_writeint
 mov eax, newline_str
 call io_writestr

 ; Write pi
 mov eax, [pi]
 call io_writeint
 mov eax, newline_str
 call io_writestr

 ; Write a
 mov eax, [a]
 call io_writeint
 mov eax, newline_str
 call io_writestr

 ; Write b
 mov eax, [b]
 call io_writeint
 mov eax, newline_str
 call io_writestr

 ; Write c
 mov eax, [c]
 call io_writeint
 mov eax, newline_str
 call io_writestr

 ; Write d
 mov eax, [d]
 call io_writeint
 mov eax, newline_str
 call io_writestr

 ; Write f
 mov eax, [f]
 call io_writeint
 mov eax, newline_str
 call io_writestr

section .data
 d dd 'd = ', 0
 f dd 'f = ', 0
 area dd 'area = ', 0
 pi dd 'pi = ', 0
 perim dd 'perim = ', 0
 radius dd 'radius = ', 0
 a dd 'a = ', 0
 b dd 'b = ', 0
 c dd 'c = ', 0
 newline_str dd 10, 0