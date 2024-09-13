import sys,os,getpass,yaml
import tkinter as tk

currentUser = getpass.getuser()
print(currentUser)

currentDir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, f"{currentDir}\\preProgram")

import validatemodules # type: ignore
validatemodules.get_requirements()

from getsettings import data # type: ignore

print(f"""
-=====================================---
Server Installers | v. {data['version']['main-build']}
Hansel Chavez (\033[94m@tardiobscurus\033[0m in discord)
-=====================================---
""")

modsFolder = f"C:\\Users\\{currentUser}\\AppData\\Roaming\\.minecraft\\mods"
if not os.path.isdir(modsFolder):
    print(f"Adding the mods folder under\nC:\\Users\\{currentUser}\\AppData\\Roaming\\.minecraft\\mods")
    with open(f"{currentDir}\\preProgram\\settings.yaml", "w") as file:
        data["mod-dir"] = modsFolder
        yaml.dump(data, file)
    os.mkdir(modsFolder)

import mainprogram # type: ignore
mainprogram.App(tk.Tk())

tk.mainloop()