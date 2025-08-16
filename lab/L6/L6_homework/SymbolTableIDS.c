#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "SymbolTableIDS.h"

#define TABLE_SIZE 100

// void initializeSymbolTableIDS(SymbolTableIDS *table)
// {
//     table->size = TABLE_SIZE;
//     for (int i = 0; i < TABLE_SIZE; i++)
//     {
//         table->symbols[i] = NULL;
//     }
// }

// Function to calculate the hash value for a name
int hashFunctionIDS(const char *name)
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
int insertID(SymbolTableIDS *table, const char *name)
{
    int index = hashFunctionIDS(name);

    // Check if the name already exists in the linked list
    SymbolEntryID *current = table->symbols[index];
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
    SymbolEntryID *newEntry = malloc(sizeof(SymbolEntryID));
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
int findID(SymbolTableIDS *table, const char *name)
{
    int index = hashFunctionIDS(name);
    SymbolEntryID *current = table->symbols[index];

    if (current != NULL)
    {
        return index;
    }

    return -1; // Symbol not found
}

// Function to print the contents of the symbol table
void printIDS(SymbolTableIDS *table)
{
    printf("section .data\n");
    for (int i = 0; i < table->size; i++)
    {
        SymbolEntryID *current = table->symbols[i];
        while (current != NULL)
        {
            // printf("atom = %s ---- cod_ts = %d\n", current->name, i);
            printf(" %s dd '%s = ', 0\n", current->name, current->name);
            current = current->next;
        }
    }
}

// Function to clean up the memory used by the symbol table
void cleanupIDS(SymbolTableIDS *table)
{
    for (int i = 0; i < table->size; i++)
    {
        SymbolEntryID *current = table->symbols[i];
        while (current != NULL)
        {
            SymbolEntryID *next = current->next;
            free(current);
            current = next;
        }
    }
}

void simplePrintIDS()
{
    printf("Hi from SymbolTableIDS.c\n");
}