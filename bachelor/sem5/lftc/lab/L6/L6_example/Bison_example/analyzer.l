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

REAL_NUMBER  -?([0-9]+|[0-9]*\.[0-9]+([eE][-+]?[0-9]+)?)
ID [a-z][a-z_]*
SUFIX   ((u|U)?(l|L)?(l|L)?)|((l|L)?(l|L)?(u|U)?)
BINAR   (0b|0B)(0|1)+{SUFIX}
OCTA    0[0-7]*{SUFIX}
HEXA    0(x|X)[0-9A-Ea-e]+{SUFIX}

%%
cin            { return CIN; }
">>"           { return CINOPP; }
";"            { return SEMICOLON; }

{ID}{0,255}     {
                return ID;
}
{REAL_NUMBER}|{BINAR}|{OCTA}|{HEXA}     {
                        return CONSTANT;
}
[\n]            { currentLine++; }

[ \t]+ ;

%%