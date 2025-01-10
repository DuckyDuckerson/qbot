#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

// Variables---------------------------------------------------------------
char *name;
int inventory[10];
// ------------------------------------------------------------------------


// functions --------------------------------------------------------------
void printing(int index, const char *message, float delay) 
{
    if (index < strlen(message)) 
    {
        putchar(message[index]);
        fflush(stdout);
        usleep((int)(delay * 1000000)); // convert delay to microseconds
        printing(index + 1, message, delay);
    }
}


void print_message(const char *message, int speed, int newline) 
{
    float speed_map[6] = {0, 0.2, 0.05, 0.01, 0.007, 0.003};
    float delay = speed_map[speed];
     
    printing(0, message, delay);
      
    if (newline == 1) 
    {
        putchar('\n');
    }
}


void save_game()
{
    FILE *file = fopen("savegame.txt", "w");
    if (file == NULL)
    {
        printf("Error opening file for writing.\n");
        return;
    }

    // Write the inventory to the file
    for (int i = 0; i < 10; i++)
    {   
        fprintf(file, "%d\n", inventory[i]);
        fprintf(file, "%s\n", name);
    }

    fclose(file);
}


void save_check()
{
    if (access("savegame.txt", F_OK) != -1) 
    {
        print_message("There is a save file, do you want to load it? (1. Yes, 2. No)", 4, 1);
        if (getchar() == '1')
        {
            FILE *file = fopen("savegame.txt", "r");
            if (file == NULL)
            {
                printf("Error opening file for reading.\n");
                return;
            }

            // Read the inventory from the file
            for (int i = 0; i < 10; i++)
            {   
                fscanf(file, "%d\n", &inventory[i]);
                fscanf(file, "%s\n", name);
            }

            fclose(file);
        }

        else 
        {
            print_message("Do you want to delete the save file? (1. Yes, 2. No)", 4, 1);
            if (getchar() == '1')
            {
                remove("savegame.txt");
                print_message("Save file deleted.", 4, 1);
                
                print_message("What is your name?", 4, 1);
                fscanf(stdin, "%s", name);
                save_game();
            }

            else {
                print_message("Continuing without loading save file.", 4, 1);
                
                print_message("What is your name?", 4, 1);
                fscanf(stdin, "%s", name);
                save_game();
            }
        }
    }

    else 
    {
        print_message("What is your name?", 4, 1);
        fscanf(stdin, "%s", name);
        save_game();
    }
}
// ------------------------------------------------------------------------

// Story functions --------------------------------------------------------
void intro()
{
    print_message("The year is 2094", 2, 1);
    print_message("...", 1, 1);

    print_message("Hurricanes threaten the NEA's capital Anchorage", 2, 1);
    print_message("North Enterpise Alliance", 5,1);
    print_message("...", 1, 1);

    print_message("The NEA is a government formed by corporations after the United States of America fell from internal conflict", 2, 1);
    print_message("The NEA took over the western states and western Canada", 2, 1);
    print_message("...", 1, 1);

    print_message("You are a citizen of the NEA", 2, 1);
    print_message("You are living in a small apartment in Anchorage", 2, 1);
    print_message("This apartment is created from a shipping container", 2, 1);
    print_message("The building has a movable crane that can move the container apartments around", 2, 1);
    print_message("Your apartment is on the 9th floor", 2, 1);
    print_message("You have no windows in your container, only a small balcony you get to by opening the back doors of the container", 2, 1);
    print_message("...", 1, 1);

    save_check();
}


void apartment()
{
    print_message("You are home.", 3, 1);
}


// ------------------------------------------------------------------------
int main() 
{ 
    print_message("Welcome to the game", 3, 1);
    print_message("...", 1, 1);

    print_message("Do you want to play the intro? (1. Yes, 2. No)", 3, 1);
    if (getchar() == '1')
    {
        intro();
        apartment();
    }
    else 
    {
        print_message("Skipping intro...", 3, 1);
        apartment();
    }

    
    


    return 0;
}
