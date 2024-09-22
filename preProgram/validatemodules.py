needed_modules = {
    "tk": ">=0.1.0",
    "gdown": ">=5.2.0",
    "pyyaml": ">=6.0.0",
}
import subprocess, sys

def install_pip(package, version):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', f"{package}{version}"])

def get_requirements():
    print(f"Double checking if your system have the required files...")
    spec = subprocess.check_output([sys.executable, "-m", "pip", "freeze"])
    installed_packages = [r.decode().split('==')[0] for r in spec.split()]
    for (package, version) in needed_modules.items():
        if package not in installed_packages:
            install_pip(package, version)
