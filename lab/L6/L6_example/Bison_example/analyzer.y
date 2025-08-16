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
%token SEMICOLON
%token CINOPP
%token CIN

%%
program: CIN CINOPP ID SEMICOLON
		{
			printf("
                mov eax, str_a \n 
                call io_writestr \n 
                call io_readint \n 
                mov ebx, eax \n
            ");
		}
       ;
%%

int main(int argc, char* argv[]) {
	printf("\%include 'io.inc'\n global main \n section .text \n main:\n");
    ++argv, --argc;

    // sets the input for flex file
    if (argc > 0)
        yyin = fopen(argv[0], "r");
    else
        yyin = stdin;

    //read each line from the input file and process it
    while (!feof(yyin)) {
        yyparse();
    }
    printTS();
    printFIP();
    printf("section .data \n str_a  db 'A = ', 0");
    return 0;
}

void yyerror(char *s) {
    printTS();
    printFIP();
    extern char* yytext;
    printf("Error for symbol %s at line: %d ! \n",yytext, currentLine);
    exit(1);
}