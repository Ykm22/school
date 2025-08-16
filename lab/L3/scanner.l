/*** Definition Section ***/
%{
#include <string.h>
#include <stdbool.h>
#include "SymbolTableIDS.h"
#include "SymbolTableCONSTS.h"

int errorFound = 0;
int lineNumber = 1;

typedef struct FIP{
	char atom[100];
	int codAtom;
	int codTS;
}FIP;

// Init FIP
const int MAX_FIP_SIZE = 300;
FIP fip[300];
int fip_size = 0;

// Init SymbolTables
// IDS
SymbolTableIDS tableIDS;

// CONSTS
SymbolTableCONSTS tableCONSTS;

void addToFIP(const char atom[], int codAtom, int codTS) {
    if(fip_size >= MAX_FIP_SIZE) {
        printf("Reached maximum fip size: %d\n", MAX_FIP_SIZE);
        exit(1);
    }
    bool exists_already = 0;
    for(int i = 0; i < fip_size && exists_already == 0; i++) {
        const char* current_atom = fip[i].atom;
        if(strcmp(current_atom, atom) == 0) {
            exists_already = 1;
        }
    }
    if(!exists_already) {
        strcpy(fip[fip_size].atom, atom);
        fip[fip_size].codAtom = codAtom;
        fip[fip_size].codTS = codTS;

        fip_size++; 
    }
}

int addToTSCONSTS(const char *name) {
    // printf("added %s to consts\n", name);
	int codTS = insertCONST(&tableCONSTS, name);
    addToFIP(name, 1, codTS);
    return codTS;
}

int addToTSIDS(const char* name) {
    // printf("added %s to ids\n", name);
    int codTS = insertID(&tableIDS, name);
    addToFIP(name, 0, codTS);
    return codTS;
}

void printTS() {
    printf("ID SymbolTable ------------------- \n");
    printIDS(&tableIDS);
    printf("\nCONSTS SymbolTable -------------------\n");
    printCONSTS(&tableCONSTS);
}

void cleanup() {
    cleanupCONSTS(&tableCONSTS);
    cleanupIDS(&tableIDS);
}

void printFIP() {
    printf("FIP -----------\n");
    for(int i = 0; i < fip_size; i++) {
        FIP current_atom = fip[i];
        printf("atom = %s --- cod atom = %d --- cod TS = %d\n", current_atom.atom, current_atom.codAtom, current_atom.codTS);
    }
    printf("\n");
}

%}

INT_NUMBER    [+-]?[0-9]+
HEXA_NUMBER   0[xX][0-9a-fA-F]+
BINARY_NUMBER 0[bB][01]+
OCTAL_NUMBER  0[oO]?[0-7]+
FLOAT_NUMBER  [+-]?([0-9]*[.])?[0-9]+([eE][+-]?[0-9]+)?

IDENTIFIER    [A-Za-z][A-Za-z0-9]{0,7}
ILLEGAL_ID    [A-Za-z0-9]{9,}

STRING        \".*\"

/*** Rule Section ***/
%%
					/* yytext is the text in the buffer */
"#include <iostream>"					{ addToFIP(yytext, 30, -1); }
"using namespace std"                   { addToFIP(yytext, 31, -1); }
main                                    { addToFIP(yytext, 35, -1); }
if                                    	{ addToFIP(yytext, 29, -1); }
while                                   { addToFIP(yytext, 2, -1); }
for                                    	{ addToFIP(yytext, 3, -1); }
write                                   { addToFIP(yytext, 4, -1); }
read                                    { addToFIP(yytext, 5, -1); }
else                                    { addToFIP(yytext, 6, -1); }
int                                    	{ addToFIP(yytext, 7, -1); }
real                                   	{ addToFIP(yytext, 8, -1); }
char									{ addToFIP(yytext, 9, -1); }
\<                                    	{ addToFIP(yytext, 21, -1); }
\<{2}									{ addToFIP(yytext, 10, -1); }
\;                                    	{ addToFIP(yytext, 11, -1); }
\(                                    	{ addToFIP(yytext, 12, -1); }
\)                                    	{ addToFIP(yytext, 13, -1); }
\,                                    	{ addToFIP(yytext, 14, -1); }
\+                                    	{ addToFIP(yytext, 15, -1); }
\-                                    	{ addToFIP(yytext, 16, -1); }
\*                                    	{ addToFIP(yytext, 17, -1); }
\/                                    	{ addToFIP(yytext, 18, -1); }
\%                                    	{ addToFIP(yytext, 19, -1); }
\>                                    	{ addToFIP(yytext, 20, -1); }
\>=                                    	{ addToFIP(yytext, 22, -1); }
\=                                    	{ addToFIP(yytext, 23, -1); }
\==                                     { addToFIP(yytext, 24, -1); }
\and                                    { addToFIP(yytext, 25, -1); }
\or                                     { addToFIP(yytext, 26, -1); }
\.                                      { addToFIP(yytext, 27, -1); }
\!=                                     { addToFIP(yytext, 28, -1); }
\{                                      { addToFIP(yytext, 32, -1); }
\}                                      { addToFIP(yytext, 33, -1); }
\;                                      { addToFIP(yytext, 34, -1); }
daca                                    { addToFIP(yytext, 35, -1); }
atunci                                  { addToFIP(yytext, 36, -1); }
sfdaca                                  { addToFIP(yytext, 37, -1); }
{INT_NUMBER}                            { addToTSCONSTS(yytext); }
{HEXA_NUMBER}                           { addToTSCONSTS(yytext); }
{BINARY_NUMBER}                         { addToTSCONSTS(yytext); }
{OCTAL_NUMBER}                          { addToTSCONSTS(yytext); }
{FLOAT_NUMBER}                          { addToTSCONSTS(yytext); }
{STRING}								{ addToFIP(yytext, 35, -1); }
{IDENTIFIER}							{ addToTSIDS(yytext); }
{ILLEGAL_ID}                            { errorFound = 1; printf("Illegal token %s at line %d !", yytext, lineNumber); return 0; }
[\n]									{ ++lineNumber; }
[ \t\n]+             					{ ; /* eat up whitespace */ }
<<EOF>>									{ printFIP(); printTS(); cleanup(); return 0; }
.                						{ errorFound = 1; printf("Illegal token %s at line %d !", yytext, lineNumber); return 0; }
%%

/* yywrap() - wraps the above rule section */
int yywrap() {}

int main(int argc, char** argv) {

	FILE *fp;
	fp = fopen(argv[1], "r");
	
	/* yyin - takes the file pointer which contains the input*/
	yyin = fp;
    
    initializeSymbolTableIDS(&tableIDS);
    initializeSymbolTableCONSTS(&tableCONSTS);

	/* yylex() - this is the main flex function which runs the Rule Section*/ 
	// check for EOF with != 0
	while( yylex() != 0) {}

    if(errorFound != 0) {
        return 0;
    }

	fclose(fp);

	return 0;
}