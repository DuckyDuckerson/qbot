import sys
import time


def print_message(message, speed, newline):

    speed_map = {
        1: .2,
        2: .05,
        3: .01,
        4: .007
    }

    delay = speed_map[speed]

    printing(0, message, delay)

    if newline == 1:
        print('\n')
    else:
        pass


def printing(index, message, delay):

    if index < len(message):
        sys.stdout.write(message[index])
        sys.stdout.flush()
        time.sleep(delay)

        printing(index + 1, message, delay)
