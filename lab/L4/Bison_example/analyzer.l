%{
#include "analyzer.tab.h"
int currentLine=1;

#include <string.h>
#include <stdlib.h>

void addToFIP(char atom[], int codAtom,int codTS)
{
}

int addToTS(char atom[])
{
	return 0;
}
void printTS()
{
}

void printFIP()
{
}
%}

%option noyywrap

INT_NUMBER    [+-]?[0-9]+
HEXA_NUMBER   0[xX][0-9a-fA-F]+
BINARY_NUMBER 0[bB][01]+
OCTAL_NUMBER  0[oO]?[0-7]+
FLOAT_NUMBER  [+-]?([0-9]*[.])?[0-9]+([eE][+-]?[0-9]+)?

IDENTIFIER    [A-Za-z][A-Za-z0-9]{0,7}
ILLEGAL_ID    [A-Za-z0-9]{9,}

%%
if              { addToFIP(yytext, 2, -1); printf("%s added to fip \n", yytext); return IF; }
else            { addToFIP(yytext, 3, -1);printf("%s is simbol \n", yytext); return ELSE; }
while           { addToFIP(yytext, 4, -1); printf("%s is simbol \n", yytext); return WHILE;  }
"/"             { addToFIP(yytext,27,-1); printf("%s is simbol \n", yytext); return DIVID;  }
"<"             { addToFIP(yytext,31,-1); printf("%s is simbol \n", yytext); return LT;   }
">"             { addToFIP(yytext,32,-1); printf("%s is simbol \n", yytext); return GT;  }
"("|")"         { addToFIP(yytext,33,-1); printf("%s is simbol \n", yytext); return PARAN; }
"{"|"}"         { addToFIP(yytext,34,-1); printf("%s is simbol \n", yytext); return BRACE; }
"["|"]"         { addToFIP(yytext,35,-1); printf("%s is simbol \n", yytext); return SQUARE; }
":"             { addToFIP(yytext,36,-1); printf("%s is simbol \n", yytext); return COLON; }
";"             { addToFIP(yytext,37,-1); printf("%s is simbol \n", yytext); return SEMICOLON; }
","             { addToFIP(yytext,38,-1); printf("%s is simbol \n", yytext); return COMMA; }
"."             { addToFIP(yytext,39,-1); printf("%s is simbol \n", yytext); return PERIOD; }
"="             { addToFIP(yytext,40,-1); printf("%s is simbol \n", yytext); return ASSIGN; }
"+"             { addToFIP(yytext,41,-1); printf("%s is simbol \n", yytext); return PLUS; }
"-"             { addToFIP(yytext,42,-1); printf("%s is simbol \n", yytext); return MINUS; }
"*"             { addToFIP(yytext,43,-1); printf("%s is simbol \n", yytext); return MUL; }
"!="            { addToFIP(yytext,44,-1); printf("%s is simbol \n", yytext); return NE; }
"=="            { addToFIP(yytext,45,-1); printf("%s is simbol \n", yytext); return EQ; }


{IDENTIFIER}    { printf("%s is id\n", yytext); return ID;}
{INT_NUMBER}|{HEXA_NUMBER}|{BINARY_NUMBER}|{OCTAL_NUMBER}|{FLOAT_NUMBER} {
                return CONSTANT;
}
[\n]            { currentLine++; }

[ \t]+ ;
%%