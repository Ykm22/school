#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "SymbolTableCONSTS.h"

#define TABLE_SIZE 100

void initializeSymbolTableCONSTS(SymbolTableCONSTS *table)
{
    table->size = TABLE_SIZE;
    for (int i = 0; i < TABLE_SIZE; i++)
    {
        table->symbols[i] = NULL;
    }
}

// Function to calculate the hash value for a name
int hashFunctionCONST(const char *name)
{
    int total = 0;
    while (*name)
    {
        total += *name;
        name++;
    }
    return total % TABLE_SIZE;
}

// Function to insert a symbol into the symbol table
int insertCONST(SymbolTableCONSTS *table, const char *name)
{
    int index = hashFunctionCONST(name);

    // Check if the name already exists in the linked list
    SymbolEntryCONST *current = table->symbols[index];
    while (current != NULL)
    {
        if (strcmp(current->name, name) == 0)
        {
            // Name already exists, no need to insert
            return index;
        }
        current = current->next;
    }

    // Name not found, proceed with the insertion
    SymbolEntryCONST *newEntry = malloc(sizeof(SymbolEntryCONST));
    if (newEntry == NULL)
    {
        perror("Memory allocation failed");
        exit(EXIT_FAILURE);
    }

    strcpy(newEntry->name, name);
    newEntry->next = NULL;

    if (table->symbols[index] == NULL)
    {
        // No collision, insert at the beginning of the list
        table->symbols[index] = newEntry;
    }
    else
    {
        // Collision, append to the end of the list
        current = table->symbols[index];
        while (current->next != NULL)
        {
            current = current->next;
        }
        current->next = newEntry;
    }
    return index;
}

// Function to find a symbol in the symbol table
int findCONST(SymbolTableCONSTS *table, const char *name)
{
    int index = hashFunctionCONST(name);
    SymbolEntryCONST *current = table->symbols[index];

    if (current != NULL)
    {
        return index;
    }

    return -1; // Symbol not found
}

// Function to print the contents of the symbol table
void printCONSTS(SymbolTableCONSTS *table)
{
    for (int i = 0; i < table->size; i++)
    {
        SymbolEntryCONST *current = table->symbols[i];
        while (current != NULL)
        {
            printf("atom = %s ---- cod_ts = %d\n", current->name, i);
            current = current->next;
        }
    }
}

// Function to clean up the memory used by the symbol table
void cleanupCONSTS(SymbolTableCONSTS *table)
{
    for (int i = 0; i < table->size; i++)
    {
        SymbolEntryCONST *current = table->symbols[i];
        while (current != NULL)
        {
            SymbolEntryCONST *next = current->next;
            free(current);
            current = next;
        }
    }
}

void simplePrintCONSTS()
{
    printf("Hi from SymbolTableCONSTS.c\n");
}