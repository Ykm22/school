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

%token ID
%token CONSTANT
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
%%
// activitate
// program2: expr_list;
// expr_list: expr SEMICOLON | expr SEMICOLON expr_list;
// expr: OPENED_PARAN expr CLOSED_PARAN | OPENED_PARAN anything_list CLOSED_PARAN | OPENED_PARAN CLOSED_PARAN;
// anything_list: anything | anything anything_list;
// anything: CONSTANT | MUL;

// tema
program: library_import_list using_namespace_list ANTHET body;

library_import_list: library_import | library_import library_import_list;
library_import: INCLUDE;

using_namespace_list: using_namespace | using_namespace using_namespace_list;
using_namespace: USING SEMICOLON;

body: OPENED_BRACE instr_list return CLOSED_BRACE;

return: RETURN SEMICOLON;

instr_list: instr | instr instr_list;
instr: declaration | read | print | assign;

declaration: type declaration_list SEMICOLON;
declaration_list: ID | ID COMMA declaration_list;
type: INT | FLOAT | ID

read: CIN read_list SEMICOLON;
read_list: read_item | read_item read_list
read_item: IN_OPERATOR ID;

print: COUT print_list SEMICOLON;
print_list: print_item | print_item print_list
print_item: OUT_OPERATOR print_type;
print_type: ID | CONSTANT | STRING;

assign: ID ASSIGN expr SEMICOLON;
expr: ID | CONSTANT | expr_result;
expr_result: expr op expr;
op: PLUS | MINUS | DIVID | MOD | MUL;


%%

int main(int argc, char* argv[]) {
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
    printFIP();
    printTS();
    printf("The file is sintactically correct!\n");
    return 0;
}

void yyerror(char *s) {
    printTS();
    printFIP();
    extern char* yytext;
    printf("Error for symbol %s at line: %d ! \n",yytext, currentLine);
    exit(1);
}