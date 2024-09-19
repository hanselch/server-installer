needed_modules = {
    "tk",
    "gdown",
    "pyyaml",
}

import subprocess, sys, importlib.util

def install_pip(package):
    subprocess.run([sys.executable, '-m', 'pip', 'install', package, '--quiet'])

def get_requirements():
    print(f"Double checking if your system have the required files...")
    for package in needed_modules:
        if importlib.util.find_spec(package) is None:
            install_pip(package)
    print("")
