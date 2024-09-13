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

        self.static_top()
        self.option_window(0)

    def static_top(self):
        self.master.title(f"Server Installer | v. {current_version}")
        ttk.Label(self.master, text=f"Server Installer v. {current_version}", 
                 font=("Arial", 15)).grid(row=0)

    def option_window(self, column):
        ttk.Label(self.master, text="What would you like to do?").grid(column=column,row=1)
        options = {"Setup Mods": 1, "Setup Shaders": 2, "Install World": 3}
        self.chosenOption = tk.StringVar()
        irow = 2
        for (text, value) in options.items():
            selectedOption = ttk.Radiobutton(self.master, text = text, width=15,
                                             value=value,
                                             variable=self.chosenOption)
            selectedOption.grid(column=column, row=irow)
            if data["shaders-installed"] == False and text == "Setup Shaders":
                selectedOption.config(state="disabled")
            else:
                selectedOption.config(state="normal")
            irow+=1
        
        ttk.Button(self.master, text="Go!", command=self.selected).grid(column=column, row=irow+1)

    def selected(self):
        program = int(self.chosenOption.get())

        if program == 1:
            self.installing_mods()
        elif program == 2:
            self.installing_shaders()
        elif program == 3:
            self.installing_world()
    
    def installing_mods(self):
        mod_installer_app = tk.Toplevel(self.master)
        mod_installer_app.title("Mod Loader v.1")
        
        ttk.Separator()

        self.modsDir = ttk.Entry(mod_installer_app, width=50)
        self.modsDir.grid(column=0, columnspan=3, row=1)
        self.modsDir.insert(0,data["mod-dir"])
        ttk.Button(mod_installer_app, text="...", command=self.choose_dir).grid(column=3,row=1)
        
        ttk.Separator()

        installation_option = {
            "Install Mods": "install",
            "Update Mods": "update",
            "Delete Mods (Debug)": "delete",
        }
        ttk.Label(mod_installer_app, text="What would you like to do?").grid(column=1,row=2)
        irow = 3
        self.chosenType = tk.StringVar()
        for (text, value) in installation_option.items():
            type = ttk.Radiobutton(mod_installer_app, text=text, value=value, variable=self.chosenType, width=20)
            type.grid(column=1, row=irow)
            irow += 1
        
        shaders_options = {
            "Yes": 1,
            "No": 0,
        }
        ttk.Label(mod_installer_app, text="Shaders?").grid(column=2,row=2)
        irow = 3
        self.addShaders = tk.StringVar()
        if data["shaders-installed"] == True:
            self.addShaders = tk.StringVar(value=1)
        elif data["shaders-installed"] == False:
            self.addShaders = tk.StringVar(value=0)
        for (text, value) in shaders_options.items():
            shaders = ttk.Radiobutton(mod_installer_app, text=text, value=value, variable=self.addShaders, width=10)
            shaders.grid(column=2,row=irow)
            irow +=1

        ttk.Separator()

        def whatNext():
            type = self.chosenType.get()
            shaders = int(self.addShaders.get())
            dir = self.modsDir.get()
            
            if type == "install":
                self.install_mods(dir, shaders)
            elif type == "update":
                self.update_mods(dir, shaders)
            elif type == "delete":
                self.delete_mods(dir)
            else:
                messagebox.askokcancel(message="You need to choose the type of installation.")
                
            if len(dir) == 0:
                messagebox.askokcancel(message="You need to enter the location of the mods folder to continue.")

        ttk.Button(mod_installer_app, text="Go!", command=whatNext).grid(column=1,columnspan=2,row=7)
    
    def installing_shaders(self):
        messagebox.askokcancel(message="As of v0.1-alpha, this option is not available yet.")
    def installing_world(self):
        messagebox.askokcancel(message="As of v0.1-alpha, this option is not available yet.")
    
    def install_mods(self, mod_directory, add_shaders):
        if any(pathlib.Path(mod_directory).iterdir()):
            filesInDir = glob.glob(mod_directory+"/*")
            print(filesInDir)
            saveMods =  messagebox.askyesno(message="To continue forwards, we need the mods folder to be empty. Would you like to save the current mods you have in the folder, in a seperate zip file?")
            if saveMods:
                print("Making zip file for old mods")
                shutil.make_archive("oldMods", 'zip', self.currentDir)
                print(f"Made {self.currentDir}/oldMods.zip")

                print("")

                print("Deleting mods in selected mods folder...")
                for mod in filesInDir:
                    os.remove(mod)

        Shaders = None
        if add_shaders == 1:
            Shaders = True
            if data["shaders-installed"] == False:
                print("The data says it's you should not install")
                setShader = messagebox.askyesno(message="Would you like to set default on shaders (add shaders) for future installation?")
                if setShader:
                    print("Setting the data to match installation to true")
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
        print("Downloading the `mods.zip`, from google drive.")
        gdown.download(data["drive-url"]["main-mods-zip"], zipfile_dir, fuzzy=True)
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
            
    def choose_dir(self):
        selectedModsDir = filedialog.askdirectory(initialdir=data["mod-dir"], mustexist=True)

        self.modsDir.delete(0,END)
        self.modsDir.insert(0,selectedModsDir)

        if selectedModsDir != data["mod-dir"]:
            setDefault = messagebox.askyesno(message=f"The directory below, is not set as a default:\n{selectedModsDir}\nWould you like to set it as a default to your `settings.yaml` file?")
            
            if setDefault == True:
                with open(f"{self.currentDir}\\settings.yaml", "w") as file:
                    data["mod-dir"] = selectedModsDir
                    yaml.dump(data, file)