#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

// Variables---------------------------------------------------------------
int apartment_v = 0;
int hideout_v = 1;
int lobby_v = 2;
int street_v = 3;
int coffee_shop_v = 4;
int alley_v = 5;
// ------------------------------------------------------------------------
int inventory[10];
int apartment1st;
// ------------------------------------------------------------------------

// Function prototypes ----------------------------------------------------
void last_location();
void intro();
void apartment();
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
    else 
    {
        putchar(' ');
    }
}


// Save list --------------------------------------------------------------
int save_list[10];
// location, apartment1st,
// ------------------------------------------------------------------------
void save_game()
{
    FILE *file = fopen("savegame.txt", "w");
    if (file == NULL)
    {
        printf("Error opening file for writing.\n");
        return;
    }
    else
    {   
        print_message("Saving game.", 4, 1);
        for (int i = 0; i < 10; i++)
        {   
            fprintf(file, "%d\n", save_list[i]);
        }

        fclose(file);
    }
    
}


void load_game()
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
                save_game();
                print_message("New save created.", 4, 1);
                intro();
                apartment();
            }
            
            print_message("Loading save file.", 4, 1);
            for (int i = 0; i < 10; i++)
            {   
                fscanf(file, "%d", &save_list[i]);
            }

            last_location();

            fclose(file);
        }

        else 
        {
            print_message("Deleting save file.)", 4, 1);
            remove("savegame.txt");
            print_message("Save file deleted.", 4, 1);
            save_game();
            print_message("New save created.", 4, 1);
            intro();
            apartment();
        }
    }

    else 
    {
        save_game();
        print_message("New save created.", 2, 1);
        intro();
        apartment();
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
}


void chapter1()
{
    print_message("You step out of your apartment", 2, 1);
    print_message("You walk down the stairs to the ground floor", 2, 1);
    print_message("You walk out of the building", 2, 1);
    print_message("...", 1, 1);
}


void apt_explore()
{
    print_message("1. A bed", 3, 1);
    print_message("2. A small kitchen", 3, 1);
    print_message("3. A bathroom", 3, 1);
    print_message("4. A closet", 3, 1);
    print_message("5. A small table", 3, 1);
    print_message("6. A computer", 3, 1);
    print_message("7. Front door", 3, 1);
    print_message("8. Balcony door", 3, 1);
    print_message("...", 1, 1);

    print_message("What do you want to interact with?", 2, 1);

    char choice = getchar();
    if (choice == 1)
    {
        print_message("You go to bed", 2, 1);
        print_message("...", 1, 1);

        // add story here
    }

    else if (choice == 2)
    {
        print_message("You go to the kitchen", 2, 1);
        print_message("...", 1, 1);
    }

    else if (choice == 3)
    {
        print_message("You go to the bathroom", 2, 1);
        print_message("...", 1, 1);
    }

    else if (choice == 4)
    {
        print_message("You go to the closet", 2, 1);
        print_message("...", 1, 1);
    }

    else if (choice == 5)
    {
        print_message("There is a note on the table", 2, 1);
        print_message("Note: When you wake up meet me in the alley", 2, 1);
        print_message("...", 1, 1);
        print_message("How did he get in here? He does not have a key...", 2, 1);
        print_message("Shit...", 2, 1);
        print_message("Well I better see what he wants.", 2, 1);
        apt_explore();
    }

    else if (choice == 6)
    {
        print_message("You go to the computer", 2, 1);
        print_message("...", 1, 1);
    }

    else if (choice == 7)
    {
        chapter1();
    }

    else if (choice == 8)
    {
        print_message("You open the heavy balcony doors,", 2, 1);
        print_message("and step out onto the small balcony.", 2, 1);
        print_message("Cold rain hits your face.", 2, 1);
        print_message("Gusts of wind try to push you back inside.", 2, 1);
        print_message("...", 1, 1);

        print_message("You can see the city infront of, and below you", 2, 1);
        print_message("The city is dark, only lit by the neon signs of the buildings", 2, 1);
        print_message("The bustling city below you can almost not be heard", 2, 1);
        print_message("through the storm.", 2, 1);

        print_message("...", 1, 1);

        print_message("Do you want to go back inside?", 3, 1);
        print_message("1. Yes", 4, 1);
        print_message("2. No", 4, 1);

        char choice = getchar();
        if (choice == 1)
        {
            print_message("You go back inside", 2, 1);
            print_message("...", 1, 1);
            apt_explore();
        }

        else 
        {
            print_message("You see a flashing light from an alley across the street.", 2, 1);
            print_message("...", 1, 1);
            print_message("Do you want to go to the alley", 2, 1);
            print_message("or go back inside?", 2, 1);
            print_message("1. Go to the alley", 4, 1);
            print_message("2. Go back inside", 4, 1);

            char choice = getchar();
            if (choice == 1)
            {
                chapter1();
            }

            else 
            {
                print_message("You go back inside", 2, 1);
                print_message("...", 1, 1);
                apt_explore();
            }
        }
    }

    else 
    {
        print_message("Invalid choice", 2, 1);
        apt_explore();
    }
}

void apartment()
{   
    int apartment1st = save_list[1];
    save_list[0] = apartment_v;

    if (apartment1st == 0)
    {
        print_message("You wake up in your apartment", 2, 1);
        print_message("You can hear the rain hitting the metal", 2, 1);
        print_message("the wind howling,", 2, 1);
        print_message("muffled by the density of the walls.", 2, 1);
        print_message("The doors on either side of the apartment", 2, 1);
        print_message("is closed and sealed so water does not get in.", 2, 1);
        print_message("...", 1, 1);

        apartment1st = 1;
        save_list[1] = apartment1st;

        save_game();

        apt_explore();
    }

    else 
    {   
        print_message("You are in your apartment", 2, 1);
        print_message("...", 1, 1);
        apt_explore();
    }   
    save_game();
}


// Location switch case ---------------------------------------------------
void last_location()
{   
    int location = save_list[0];
    switch (location)
    {
        case 0:
            apartment();
            break;
        //case 0:
        //    hideout();
        //    break;
        //case 2:
        //    lobby();
        //    break;
        //case 3:
        //    street();
        //    break;
        //case 4:
        //    coffee_shop();
        //    break;
        //case 5:
        //    alley();
        //    break;
        default:
            break;
    }
}
// ------------------------------------------------------------------------
// ------------------------------------------------------------------------
int main() 
{ 
    print_message("Welcome to Anchorage", 2, 1);
    print_message("...", 1, 1);

    load_game();

    return 0;
}
