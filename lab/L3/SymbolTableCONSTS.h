// SymbolTableCONSTS.h

#ifndef SYMBOL_TABLE_CONSTS_H
#define SYMBOL_TABLE_CONSTS_H

#define TABLE_SIZE 100

typedef struct SymbolEntryCONST
{
    char name[50];
    struct SymbolEntryCONST *next;
} SymbolEntryCONST;

typedef struct
{
    int size;
    SymbolEntryCONST *symbols[TABLE_SIZE];
} SymbolTableCONSTS;

void initializeSymbolTableCONSTS(SymbolTableCONSTS *table);
int hashFunctionCONST(const char *name);
int insertCONST(SymbolTableCONSTS *table, const char *name);
int findCONST(SymbolTableCONSTS *table, const char *name);
void printCONSTS(SymbolTableCONSTS *table);
void cleanupCONSTS(SymbolTableCONSTS *table);
void simplePrintCONSTS();
#endif
