
# Server Installer

A simple Python v3 mod installer using [Tkinter](https://tkdocs.com/resources/backgrounder.html). This is a seperate repo of the [original program](https://github.com/hanselch/mod-installer) with more features and better code.

This is was originally ment to help close friends install mods easily and get back in to the game faster! The project later evolved in to an intuative program for any modpack not using external sites, such as CurseForge or Modrinth.

For info on the program and server, go to the [wiki](https://github.com/hanselch/server-installer/wiki).

## Features

This is a very simple program adding the following:
- Setting up mods
    - Installing the mods to your mods directory
    - Updating the mods from the mods directory
    - For any issues, deleting the mods from the directory
- Installing shaders (*coming soon*)
    - Setting up a `shaderspack` directory
    - Selecting the type of PC power you have for the shaders
    - Installing/updating shaders in to that shaderspack directory
- Installing the server's world (*coming soon*)
    - Expanding on servers, for your players to install the world
    - When downloading the world, it will immediately be set to the `saves` folder

## Installation

You can install the main zip file on either the right side of this main page under the `packages` link or by clicking [here](https://github.com/hanselch/server-installer/releases).

Scroll down to find the `.zip` file, and click it to install.

After installing the `.zip` file, **YOU MUST EXTRACT THE FOLDER THAT IS IN THE `.zip` FILE**. This will make local installation on packages less confusing for the program!

---

For using the terminal, do the following.

1. Clone the directory using `git`
```sh
git clone https://github.com/hanselch/server-installer.git
```

2. Go in to the `Installer v0` folder and either open the file with you file explorer or enter:
```sh
python3 /path/to/Installer {version}
```

> [!NOTE]
> There will soon be beta testing versions in the future for code.
