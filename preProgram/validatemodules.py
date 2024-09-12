needed_modules = {
    "tk",
    "gdown",
    "pyyaml"
}

import subprocess, sys, importlib.util

def install_pip(package):
    subprocess.run([sys.executable, '-m', 'pip', 'install', package])

def get_requirements():
    print(f"Double checking if your system have the required files...")
    for package in needed_modules:
        if importlib.util.find_spec(package) is None:
            install_pip(package)
            try:
                getattr(__import__(package))
            except:
                print("Something came up in line: 20, validatemodules.py")
    print("")
