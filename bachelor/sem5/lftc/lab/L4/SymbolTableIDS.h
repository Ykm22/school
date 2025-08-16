// SymbolTableIDS.h

#ifndef SYMBOL_TABLE_IDS_H
#define SYMBOL_TABLE_IDS_H

#define TABLE_SIZE 100

typedef struct SymbolEntryID
{
    char name[8];
    struct SymbolEntryID *next;
} SymbolEntryID;

typedef struct
{
    int size;
    SymbolEntryID *symbols[TABLE_SIZE];
} SymbolTableIDS;

// void initializeSymbolTableIDS(SymbolTableIDS *table);
int hashFunctionID(const char *name);
int insertID(SymbolTableIDS *table, const char *name);
int findID(SymbolTableIDS *table, const char *name);
void printIDS(SymbolTableIDS *table);
void cleanupIDS(SymbolTableIDS *table);
void simplePrintIDS();
#endif
