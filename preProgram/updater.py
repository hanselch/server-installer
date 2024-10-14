print("Double checking for updates...")

import requests, os, shutil
from pathlib import Path
from zipfile import ZipFile
import urllib.request
from getsettings import data
import yaml

import time
from tqdm import tqdm

response = requests.get("https://api.github.com/repos/hanselch/server-installer/releases/latest")
repo_version = response.json()["name"]
asset = response.json()["assets"][0]["browser_download_url"]
current_dir = os.path.dirname(os.path.realpath(__file__))
name_file = f"{current_dir}\\{repo_version}.zip"
main_dir = Path(current_dir).parents[0]

def update():
    
    if data["version"] != repo_version:
        print("There is a new update!")
        asset_online = requests.get(asset)
        if (str(asset_online).find("200") == -1):
            print("Asset not found... continuing with program...")
        else:
            print(f"Asset found! Downloading file from {response.json()["html_url"]}...")
            urllib.request.urlretrieve(asset, name_file)
            files = [
                "mainprogram.py",
                "validatemodules.py",
                "getsettings.py",
                "ModInstallerv2.py"
            ]
            with ZipFile(name_file, "r") as object:
                print("Installing and updating file...")
                for i in tqdm(range(len(files)+1)):
                    for file in files:

                        if file == "ModInstallerv2.py":
                            file_location = f"{current_dir}/server-installer/{file}"
                            file_destination = f"{main_dir}\\{file}"
                            object.extract(f"server-installer/{file}", path=current_dir)
                        else:
                            file_location = f"{current_dir}/server-installer/preProgram/{file}"
                            file_destination = f"{current_dir}\\{file}"
                            object.extract(f"server-installer/preProgram/{file}", path=current_dir)

                        shutil.copy(file_location, file_destination)
                        time.sleep(0.125)
                print("Done downloading and updating project!")
            shutil.rmtree(f"{current_dir}\\server-installer")
            os.remove(name_file)
                
            print("Updating settings to newer version...")
            with open(f"{current_dir}\\settings.yaml", "w") as file:
                old_version = data["version"]
                data["version"] = repo_version
                yaml.dump(data, file)
                print(f"Updated {old_version} to {data["version"]}")

    else:
        print("It is up-to-date!")