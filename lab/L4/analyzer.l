%{
#include "analyzer.tab.h"

#include <string.h>
#include <stdlib.h>
#include "SymbolTableIDS.h"
#include "SymbolTableCONSTS.h"
#include <stdbool.h>

int errorFound = 0;
int currentLine = 1;

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

void initializeSymbolTableIDS()
{
    tableIDS.size = TABLE_SIZE;
    for (int i = 0; i < TABLE_SIZE; i++)
    {
        tableIDS.symbols[i] = NULL;
    }
}

// CONSTS
SymbolTableCONSTS tableCONSTS;

void initializeSymbolTableCONSTS()
{
    tableCONSTS.size = TABLE_SIZE;
    for (int i = 0; i < TABLE_SIZE; i++)
    {
        tableCONSTS.symbols[i] = NULL;
    }
}

void addToFIP(const char* atom, int codAtom,int codTS){
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

%option noyywrap

IDENTIFIER    [A-Za-z][A-Za-z0-9]{0,7}
ILLEGAL_ID    [A-Za-z0-9]{9,}

INT_NUMBER    [+-]?[0-9]+
HEXA_NUMBER   0[xX][0-9a-fA-F]+
BINARY_NUMBER 0[bB][01]+
OCTAL_NUMBER  0[oO]?[0-7]+
FLOAT_NUMBER  [+-]?([0-9]*[.])?[0-9]+([eE][+-]?[0-9]+)?


%%
"#include"[\t ]+["<]([^">]+)[>"]   {addToFIP(yytext, 46, -1); return INCLUDE; }
"using"[\t ]+"namespace"[\t ]+[a-zA-Z]+ {addToFIP(yytext, 47, -1); return USING; }
"int"[\t ]+"main"[\t ]*"("[\t ]*")" {addToFIP(yytext, 48, -1); return ANTHET; }
"return"[\t ]+0 {addToFIP(yytext, 120, -1); return RETURN; }
if              { addToFIP(yytext, 2, -1); return IF; }
else            { addToFIP(yytext, 3, -1); return ELSE; }
while           { addToFIP(yytext, 4, -1); return WHILE;  }
"/"             { addToFIP(yytext,27,-1); return DIVID;  }
"<"             { addToFIP(yytext,31,-1); return LT;   }
">"             { addToFIP(yytext,32,-1); return GT;  }
"("         { addToFIP(yytext,33,-1); return OPENED_PARAN; }
")"         { addToFIP(yytext,107,-1); return CLOSED_PARAN; }
"{"         { addToFIP(yytext,34,-1); return OPENED_BRACE; }
"}"         { addToFIP(yytext,100,-1); return CLOSED_BRACE; }
"["|"]"         { addToFIP(yytext,35,-1); return SQUARE; }
":"             { addToFIP(yytext,36,-1); return COLON; }
";"             { addToFIP(yytext,37,-1); return SEMICOLON; }
","             { addToFIP(yytext,38,-1); return COMMA; }
"."             { addToFIP(yytext,39,-1); return PERIOD; }
"="             { addToFIP(yytext,40,-1); return ASSIGN; }
"+"             { addToFIP(yytext,41,-1); return PLUS; }
"-"             { addToFIP(yytext,42,-1); return MINUS; }
"*"             { addToFIP(yytext,43,-1); return MUL; }
"!="            { addToFIP(yytext,44,-1); return NE; }
"=="            { addToFIP(yytext,45,-1); return EQ; }
"\<\<"          { addToFIP(yytext,101,-1); return OUT_OPERATOR; }
"\>\>"          { addToFIP(yytext,102,-1); return IN_OPERATOR; }
int             { addToFIP(yytext,103,-1); return INT; }         
float           { addToFIP(yytext,104,-1); return FLOAT; }
cin             { addToFIP(yytext,105,-1); return CIN; }
cout            { addToFIP(yytext,106,-1); return COUT; }
\".\"           { addToFIP(yytext,10,-1); return STRING; }
{IDENTIFIER}    { addToTSIDS(yytext); return ID;}
{INT_NUMBER}|{HEXA_NUMBER}|{BINARY_NUMBER}|{OCTAL_NUMBER}|{FLOAT_NUMBER} { addToTSCONSTS(yytext); return CONSTANT;}
[\n]            { currentLine++; }

[ \t ]+ ;
%%