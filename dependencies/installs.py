from dependencies.depinst import depend_install as pip_install


def installation():
    print("Installing dependencies...")
    pip_install('discord')
    pip_install('python-dotenv')
    pip_install('openai')
    print("Dependencies installed.")
