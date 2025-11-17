import subprocess
import sys


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


packages = ["pygame"]

for pkg in packages:
    install(pkg)

print("Setup complete. Run the game with: python main.py")
