%{
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

extern void printTS();
extern void printFIP();
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

%%
program: IF PARAN ID PARAN ELSE ID EQ CONSTANT SEMICOLON
       ;
%%

int main(int argc, char* argv[]) {
    // sets the input for flex file
    if (argc > 1)
        yyin = fopen(argv[1], "r");
    else
        yyin = stdin;

    //read each line from the input file and process it
    while (!feof(yyin)) {
        yyparse();
    }
    printTS();
    printFIP();
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