import subprocess
import sys


# ---------------------------------------------------------
def depend_install(package):
    print(f"Installing {package}")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    err = subprocess.CalledProcessError
    if err:
        print(err)
    else:
        print(f"{package} installed")
