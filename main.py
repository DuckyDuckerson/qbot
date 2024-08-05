from dependencies.installs import installation


''' To Do:
- Integrate ChatGPT
- Add a way to play music in VCs
- Add real databases for storing data
- Add currency system
- Add xp system
'''


def main():
    print("Welcome to Quack!")

    # Since this is being ran in a docker container,
    # we need to install the dependencies
    # every time the container is started.
    installation()

    # Import needs to be here
    # Do not fucking move it dumbass
    from discord_stuff.discord_main import run as run_main
    run_main()


if __name__ == "__main__":
    main()
