import sys,os
import tkinter as tk

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

if len(data['mod-dir']) == 0:
    print("-=[ \033[93mINFO\033[0m ]=-")
    print("Seems like the option in your `settings.yaml`;\n`mod-dir` has no value. Make sure to set a\ndefault for the mods directory when installing\nor updating the mods.")

import mainprogram # type: ignore
mainprogram.App(tk.Tk())

tk.mainloop()