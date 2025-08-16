%{
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

extern void printTS();
extern void printFIP();
extern void initializeSymbolTableCONSTS();
extern void initializeSymbolTableIDS();
extern int yylex();
extern int yyparse();
extern FILE* yyin;
extern int currentLine;
void yyerror(char *s);
%}
%union {
    char* str;
}

%token <str>CONSTANT
%token <str>ID

%token IF
%token ELSE
%token WHILE
%token PERIOD
%token SEMICOLON
%token COMMA
%token COLON
%token PLUS
%token MINUS
%token MUL
%token MOD
%token DIVID
%token ASSIGN
%token LT
%token GT
%token NE
%token BRACE
%token PARAN

%token SQUARE
%token JAVAUTIL
%token EQ

%token INCLUDE
%token USING
%token ANTHET
%token OPENED_BRACE
%token CLOSED_BRACE
%token INT
%token FLOAT
%token IN_OPERATOR
%token OUT_OPERATOR
%token STRING
%token CIN
%token COUT
%token RETURN

%token OPENED_PARAN
%token CLOSED_PARAN

%type <str> print_type
%%
// activitate
// program2: expr_list;
// expr_list: expr SEMICOLON | expr SEMICOLON expr_list;
// expr: OPENED_PARAN expr CLOSED_PARAN | OPENED_PARAN anything_list CLOSED_PARAN | OPENED_PARAN CLOSED_PARAN;
// anything_list: anything | anything anything_list;
// anything: CONSTANT | MUL;

// tema
program: declaration_list assign_list read_list print_list

assign_list: assign_item | assign_item assign_list;
assign_item: ID ASSIGN ID SEMICOLON 
                {
                    printf(" ; Assign to: %s, value: %s\n", $1, $3);
                    // printf(" mov dword [%s], %s\n\n", $1, $3);
                    printf(" mov eax, [%s]\n", $3);
                    printf(" mov [%s], eax\n\n", $1);
                };
            | ID ASSIGN CONSTANT SEMICOLON 
                {
                    printf(" ; Assign to: %s, value: %s\n", $1, $3);
                    printf(" mov dword [%s], %s\n\n", $1, $3);
                }
            | ID ASSIGN ID PLUS CONSTANT SEMICOLON 
                {
                    printf(" ; Assign to: %s, value: %s + %s\n", $1, $3, $5);
                    printf(" mov eax, [%s]\n add eax, %s\n mov [%s], eax \n\n", $3, $5, $1);
                }
            | ID ASSIGN ID MINUS CONSTANT SEMICOLON 
                {
                    printf(" ; Assign to: %s, value: %s\n", $1, $3);
                    printf(" mov eax, [%s]\n sub eax, %s\n mov [%s], eax \n\n", $3, $5, $1);
                }
            | ID ASSIGN ID DIVID CONSTANT SEMICOLON 
                {
                    printf(" ; Assign to: %s, value: %s / %s\n", $1, $3, $5);
                    printf(" mov eax, [%s]\n xor edx, edx\n mov ecx, %s \n div ecx \n mov [%s], eax \n\n", $3, $5, $1);
                }
            | ID ASSIGN ID MUL CONSTANT SEMICOLON 
                {
                    printf(" ; Assign to: %s, value: %s\n", $1, $3);
                    printf(" mov eax, [%s]\n imul eax, %s \n mov [%s], eax \n\n", $3, $5, $1);
                }

declaration_list: declaration | declaration declaration_list;
declaration: type ID SEMICOLON
{
    // printf("declaration-> int %s\n", $2);
};

read_list: read_item | read_item read_list;
read_item: CIN IN_OPERATOR ID SEMICOLON
{
    printf(" ; Read into %s \n mov eax, %s \n call io_writestr \n call io_readint \n mov [%s], eax \n mov eax, 0 \n\n", $3, $3, $3);
};

print_list: print_item | print_item print_list;
print_item: COUT OUT_OPERATOR print_type SEMICOLON
{
    printf(" ; Write %s \n mov eax, [%s] \n call io_writeint \n mov eax, newline_str \n call io_writestr \n\n", $3, $3);
};

// program: library_import_list using_namespace_list ANTHET body;

// library_import_list: library_import | library_import library_import_list;
// library_import: INCLUDE;

// using_namespace_list: using_namespace | using_namespace using_namespace_list;
// using_namespace: USING SEMICOLON;

// body: OPENED_BRACE instr_list return CLOSED_BRACE;

// return: RETURN SEMICOLON;

// instr_list: instr | instr instr_list;
// instr: declaration | read | print | assign;

// declaration: type declaration_list SEMICOLON;
// declaration_list: ID | ID COMMA declaration_list;
type: INT

// read: CIN read_list SEMICOLON;
// read_list: read_item | read_item read_list
// read_item: IN_OPERATOR ID;

// print: COUT print_list SEMICOLON;
// print_list: print_item | print_item print_list
// print_item: OUT_OPERATOR print_type;
print_type: ID

// assign: ID ASSIGN expr SEMICOLON;
// expr: ID | CONSTANT | expr_result;
// expr_result: expr op expr;
// op: PLUS | MINUS | DIVID | MOD | MUL;


%%

int main(int argc, char* argv[]) {
    printf("%%include 'io.inc'\n global main \n section .text \nmain:\n");
    initializeSymbolTableCONSTS();
    initializeSymbolTableIDS();
    // sets the input for flex file
    if (argc > 1)
        yyin = fopen(argv[1], "r");
    else
        yyin = stdin;

    //read each line from the input file and process it
    while (!feof(yyin)) {
        yyparse();
    }
    // printFIP();
    printTS();
    printf(" newline_str dd 10, 0\n");
    printf("The file is sintactically correct!\n");
    return 0;
}

void yyerror(char *s) {
    printTS();
    // printFIP();
    extern char* yytext;
    printf("Error for symbol %s at line: %d ! \n",yytext, currentLine);
    exit(1);
}