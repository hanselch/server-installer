needed_modules = [
    "tk",
    "gdown",
    "pyyaml",
]

import subprocess, sys

def install_pip(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def get_requirements():
    print(f"Double checking if your system have the required files...")
    spec = subprocess.check_output([sys.executable, "-m", "pip", "freeze"])
    installed_packages = [r.decode().split('==')[0] for r in spec.split()]
    for package in needed_modules:
        if package not in installed_packages:
            install_pip(package)