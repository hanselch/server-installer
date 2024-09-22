import sys,os,getpass
import tkinter as tk

currentUser = getpass.getuser()
currentDir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, f"{currentDir}\\preProgram")

from getsettings import data # type: ignore
import validatemodules # type: ignore

validatemodules.get_requirements()

import yaml

modsFolder = f"C:\\Users\\{currentUser}\\AppData\\Roaming\\.minecraft\\mods"
if not os.path.isdir(modsFolder):
    print(f"Adding the mods folder under\nC:\\Users\\{currentUser}\\AppData\\Roaming\\.minecraft\\mods")
    with open(f"{currentDir}\\preProgram\\settings.yaml", "w") as file:
        data["directories"]["mod-directory"] = modsFolder
        yaml.dump(data, file)
    os.mkdir(modsFolder)
if data["directories"]["mod-directory"] == "":
    if data["directories"]["mod-directory"] is not modsFolder:
        print(f"Adding the mods folder under\nC:\\Users\\{currentUser}\\AppData\\Roaming\\.minecraft\\mods")
        with open(f"{currentDir}\\preProgram\\settings.yaml", "w") as file:
            data["directories"]["mod-directory"] = modsFolder
            yaml.dump(data, file)
else:
    print(f"Mods folder in settings found...\n{data["directories"]["mod-directory"]}")

print(f"""
-=====================================---
Server Installers | v. {data['version']}
Hansel Chavez (\033[94m@tardiobscurus\033[0m in discord)
-=====================================---
""")

import mainprogram # type: ignore
mainprogram.App(tk.Tk())

tk.mainloop()
