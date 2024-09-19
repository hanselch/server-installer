import tkinter as tk
from tkinter import ttk, filedialog, messagebox, END
from getsettings import data
import os
import yaml # type: ignore
import gdown, zipfile, shutil, glob # type: ignore
import pathlib

current_version = data["version"]["main-build"]

class App():
    def __init__(self, master):
        self.master = master
        self.currentDir = os.path.dirname(os.path.realpath(__file__))
        super().__init__()

        # For the main window, when the user opne the program
        self.main_window(0)

    def options(self, window, options_list: dict[str, str], column: int, row: int, valVar):
        for (text,value) in options_list.items():
            option = ttk.Radiobutton(window, text=text, value=value, variable=valVar)
            option.grid(column=column, row=row)
            # for the options_window in line 34
            if data["shaders-installed"] == False and text == "Setup Shaders":
                option.config(state="disabled")
            row+=1

    def main_window(self, column):
        self.master.title(f"Server Installer | v. {current_version}")
        ttk.Label(self.master, text=f"Server Installer v. {current_version}", 
                 font=("Arial", 15)).grid(row=0)
        ttk.Label(self.master, text="What would you like to do?").grid(column=column,row=1)
        def selected():
            program = int(self.chosenOption.get())
            if program == 1:
                self.installing_mods()
            elif program == 2:
                self.installing_shaders()
            elif program == 3:
                self.installing_world()
        options = {"Setup Mods": 1, "Setup Shaders": 2, "Install World": 3}
        self.chosenOption = tk.StringVar()
        irow = 2
        self.options(self.master, options, column, irow, self.chosenOption)
        ttk.Button(self.master, text="Go!", command=selected).grid(column=column, row=5)
        
    def entryBoxDir(self, window, row, variable, type: int):
        modDirEntry = ttk.Entry(window, textvariable=variable, width=50)
        dirData = data['directories']
        # for mods dir
        if type == 1:
            if dirData["mod-directory"] != "":
                modDirEntry.insert(0, dirData["mod-directory"])
        # for shaders
        elif type == 2:
            print("for shaders")
        modDirEntry.grid(column=0, columnspan=3, row=row)

        selectedModsDirectory = None
        def getModDir():
            selectedModsDirectory = filedialog.askdirectory(initialdir="/", mustexist="true")
            if selectedModsDirectory != "":
                modDirEntry.delete(0, END)
                modDirEntry.insert(0,selectedModsDirectory)
                if selectedModsDirectory != dirData["mod-directory"]:
                    changeSetting = messagebox.askyesno(message=f"Would you like to set\n{selectedModsDirectory}\nas your new default for future installations?")
                    if changeSetting:
                        with open(f"{self.currentDir}\\settings.yaml", "w") as settings:
                            dirData["mod-directory"] = selectedModsDirectory
                            yaml.dump(data, settings)
                        
        getData = ttk.Button(window, command=getModDir, text="...")
        getData.grid(column=4, row=row)
            
    def installing_mods(self):
        mod_installer_app = tk.Toplevel(self.master)
        mod_installer_app.title("Mod Loader v1.1")

        entryVar = tk.StringVar()
        self.entryBoxDir(mod_installer_app, 0, entryVar, 1)
        
        installation_option = { "Install Mods": "install", "Update Mods": "update", "Delete Mods (Debug)": "delete"}
        ttk.Label(mod_installer_app, text="What would you like to do?").grid(column=1,row=2)
        irow = 3
        chosenType = tk.StringVar()
        self.options(mod_installer_app, installation_option, 1, irow, chosenType) 

        shaders_options = {"Yes": 1, "No": 0}
        ttk.Label(mod_installer_app, text="Shaders?").grid(column=2,row=2)
        addShaders = tk.IntVar()
        self.options(mod_installer_app, shaders_options, 2, 3, addShaders)
        if data["shaders-installed"] == True:
            addShaders.set(1)
        elif data["shaders-installed"] == False:
            addShaders.set(0)

        ttk.Separator()

        def whatNext():
            setupType = chosenType.get()
            shaders = addShaders.get()
            dir = entryVar.get()

            if len(dir) == 0:
                messagebox.askokcancel(message="You need to enter the location of the mods folder to continue.")
            else:
                if setupType == "":
                    messagebox.askokcancel(message="You need to select a 'type' of setup option to do!")
                
                if setupType == "install":
                    self.install_mods(dir, shaders)
                elif setupType == "update":
                    self.update_mods(dir, shaders)
                elif setupType == "delete":
                    self.delete_mods(dir)

        ttk.Button(mod_installer_app, text="Go!", command=whatNext).grid(column=1,columnspan=2,row=7)
    
    def installing_shaders(self):
        messagebox.askokcancel(message="As of v0.1-alpha, this option is not available yet.")
    def installing_world(self):
        messagebox.askokcancel(message="As of v0.1-alpha, this option is not available yet.")
    
    def install_mods(self, mod_directory, add_shaders: int):
        filesInDir = glob.glob(mod_directory+"/*")
        if any(pathlib.Path(mod_directory).iterdir()):
            saveMods =  messagebox.askyesno(message="To continue forwards, we need the mods folder to be empty. Would you like to save the current mods you have in the folder, in a seperate zip file?")
            if saveMods:
                print("Making zip file for old mods")
                shutil.make_archive("oldMods", 'zip', self.currentDir)
                print(f"Made {self.currentDir}/oldMods.zip")
                print("Deleting mods in selected mods folder...")
                for mod in filesInDir:
                    os.remove(mod)
            else:
                for mod in filesInDir:
                    os.remove(mod)
        Shaders = None
        if add_shaders == 1:
            Shaders = True
            if data["shaders-installed"] == False:
                setShader = messagebox.askyesno(message="Would you like to set default on shaders (add shaders) for future installation?")
                if setShader:
                    with open(f"{self.currentDir}\\settings.yaml", "w") as file:
                        data["shaders-installed"] = Shaders
                        yaml.dump(data, file)
        if add_shaders == 0:
            Shaders = False
            if data["shaders-installed"] == True:
                setShader = messagebox.askyesno(message="Would you like to set default on shaders (no shaders) for future installation?")
                if setShader:
                    with open(f"{self.currentDir}\\settings.yaml", "w") as file:
                        data["shaders-installed"] = Shaders
                        yaml.dump(data, file)
        zipfile_dir = mod_directory+"\\mods.zip"
        print("Downloading the `mods.zip`, from google drive.")
        gdown.download(data["drive-url"]["main-mods-zip"], zipfile_dir, fuzzy=True)
        print(f"Downloaded, {mod_directory}!")
        # Unzip and add to folder
        print("Extracting `mods.zip` folder.")
        with zipfile.ZipFile(zipfile_dir, 'r') as zip_file:
            zip_file.extractall(mod_directory)
        os.remove(zipfile_dir)
        print("Removed the `mods.zip` folder...")
        # Checking if the folder contains the files, based on whether the user wanted shaders or not
        if Shaders:
            os.remove(mod_directory+"\\"+data["mods-to-delete"]["with-shaders"])
            print(f"Deleted, {data['mods-to-delete']['with-shaders']}")
        else:
            for i in data["mods-to-delete"]["without-shaders"]:
                os.remove(mod_directory+"\\"+i)
                print(f"Deleted, {i}")
        messagebox.askokcancel(message="Mods are successfully installed in your mods folder!\nClosing the program, now.")
        self.master.destroy()
        
    def update_mods(self, mod_directory, add_shaders):
        zipfile_dir = mod_directory+"\\mods.zip"
        print("Deleting the original mods...")
        filesInDir = glob.glob(mod_directory+"/*")
        for mod in filesInDir:
            os.remove(mod)
        print("Downloading the `mods.zip`, from google drive.")
        gdown.download(data["drive-url"]["main-mods-zip"], zipfile_dir, fuzzy=True)
        print("Extracting `mods.zip` folder.")
        with zipfile.ZipFile(zipfile_dir, 'r') as zip_file:
            zip_file.extractall(mod_directory)
        os.remove(zipfile_dir)
        print(f"Downloaded, {mod_directory}!")
        if add_shaders == 1:
            os.remove(mod_directory+"\\"+data["mods-to-delete"]["with-shaders"])
            print(f"Deleted, {data['mods-to-delete']['with-shaders']}")
        elif add_shaders == 0:
            for i in data["mods-to-delete"]["without-shaders"]:
                os.remove(mod_directory+"\\"+i)
                print(f"Deleted, {i}")
        messagebox.askokcancel(message="Mods are successfully updated in your mods folder!\nClosing the program, now.")
        self.master.destroy()

    def delete_mods(self, mod_directory):
        deleteAll = messagebox.askyesno(message="You are about to delete all the mods in the selected folder. Would you like to proceed?")
        if deleteAll:
            print(f"Deleting all mods in {mod_directory}")
            filesInDir = glob.glob(mod_directory+"/*")
            for mod in filesInDir:
                os.remove(mod)
            messagebox.askokcancel(message=f"Removed all the mods in\n{mod_directory}\nClosing the program now.")
            self.master.destroy()