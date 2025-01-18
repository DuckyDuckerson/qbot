#include <stdio.h>
#include <stdlib.h>

void save_game(int *save_list, int size)
{
    // Open the file for writing (overwriting if it exists)
    FILE *file = fopen("savegame.txt", "w");
    if (file == NULL)
    {
        printf("Error opening file for writing.\n");
        return;
    }

    // Write the list to the file
    for (int i = 0; i < size; i++)
    {   
        fprintf(file, "%d\n", save_list[i]);
    }

    fclose(file);
}

int main()
{
    int size = 10;  // Example size
    int *save_list = (int *)malloc(size * sizeof(int));  // Dynamically allocate memory

    if (save_list == NULL)
    {
        printf("Memory allocation failed!\n");
        return 1;
    }

    // Initialize the list with some values
    for (int i = 0; i < size; i++)
    {
        save_list[i] = i * 10;  // Example values: 0, 10, 20, 30, etc.
    }

    // Save the game
    save_game(save_list, size);

    // Example of resizing the list using realloc (changing size)
    size = 15;  // New size
    save_list = (int *)realloc(save_list, size * sizeof(int));  // Resize memory

    if (save_list == NULL)
    {
        printf("Memory reallocation failed!\n");
        return 1;
    }

    // Initialize new elements
    for (int i = 10; i < size; i++)
    {
        save_list[i] = i * 5;  // New values for the expanded list
    }

    // Save the game again with the resized list
    save_game(save_list, size);

    // Free the dynamically allocated memory
    free(save_list);

    return 0;
}

