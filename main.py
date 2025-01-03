import subprocess
from dependencies.installs import installation


''' To Do:
- Add currency system
- Add a way to play music in VCs
- Add real databases for storing data
- Add a ranking system based on xp
'''


def main():
    print("Welcome to Quack!")

    '''
    Since this is being ran in a docker container,
    we need to install the dependencies
    every time the container is started.
    Yes I know this is inefficient, but it's how I have it set up.
    so shutup lol.
    '''

    installation()

    # Important; THIS needs to be here
    # Do not fucking move it dumbass
    from discord_stuff.discord_main import run as run_main
    run_main()


if __name__ == "__main__":

    try:
        # ----------------------------------
        print('Compiling C code...')
        subprocess.run(['gcc', '-shared', '-o', 'functions/cfuncs.so', 'functions/cfuncs.c'])
        print('C code compiled successfully!')
        # ----------------------------------

    except subprocess.CalledProcessError as e:
        print(f'Error: {e}')
        exit()

    main()
