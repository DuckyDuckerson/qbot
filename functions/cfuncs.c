#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>


int message_length(char *message) 
{
  int i = 0;
  while (message[i] != '\0') 
  {
    i++;
  }
  return i;
}


int xp_alg(char *message) 
{
  double xp;
  double modifer = 1.5;
  int ppm = 100;
  int length = message_length(message);

  xp = (length + ppm) * modifer;
  return xp;
}


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


int spin()
{
  char chars[] = {'/', '-', '\\', '|'};
  int i = 0;
  
  while (1) {
      printf("\r%c", chars[i]);
      fflush(stdout);
      usleep(50000);
      i = (i + 1) % 4;
  }
  return 0;
}


int shell_commands() 
{
  system("ls -l");
  system("pwd");
  return 0;
}

