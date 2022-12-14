#!/usr/bin/python3

import os
import shutil
import subprocess
import time
import sys


# Simply update the repo_url and repo_name when we create new repository for 
# another type of printer.
repo_url = "https://github.com/Global3DSystems/G3D-Printer-Release"
repo_name = "G3D-Printer-Release-master"
delay_sec = 2

"""
Usage: python3 set_github_update.py
For Raspberry Pi: python3.8 set_github_update.py

Run on /home/pi, the folder G3D-Printer-Release-master must be in the same directory.


This script updates the public GitHub repository, specifically by:
- Create a Release folder, delete if it exists.
- Change directory to Release folder.
- Clone https://github.com/Global3DSystems/G3D-Printer-Release 
- Rename G3D-Printer-Release to G3D-Printer-Release-master
- Change directory G3D-Printer-Release-master
- Clear the folder contents except the README.md, .git and .gitignore
  (find . ! -name ".git" ! -name ".gitignore" ! -name "README.md" -exec rm -rf {} +)
- Rename README.md to README_temp.md
- Rename .git to .git_temp
- Rename .gitignore to .gitignore_temp
- Copy all contents of the G3D-Printer-Release-master to Release/G3D-Printer-Release-master.
- The .git, .gitignore and README.md is also copied, we delete all of that then
  removed the "_temp" from previous 3 files that has been renamed.
- Delete all the .cpp and .h files.
"""


if __name__ == "__main__":

    if os.getcwd() != "/home/pi":
        print("Current directory: {}".format(os.getcwd()))
        print("Please run this script on /home/pi")
        sys.exit(0)

    if not os.path.exists(repo_name):
        print("{} folder not found in {}".format(repo_name, os.getcwd()))
        sys.exit(0)


    if os.path.exists("Release"):
        print("Deleting old Release folder...")
        time.sleep(delay_sec)
        shutil.rmtree("Release")

    print("Creating new Release folder...")
    time.sleep(delay_sec)
    os.mkdir("Release")
    os.chdir("Release")


    print("Cloning old OTA file...")
    time.sleep(delay_sec)
    git_clone_process = subprocess.run(["git", "clone", repo_url, repo_name], capture_output = True)

    if git_clone_process.returncode == 0:
        print("Old OTA file cloned.")
        time.sleep(delay_sec)
    else:
        print("Failed cloning the file, please try again.")
        sys.exit(1)

    print("Changing directory to {}".format(repo_name))
    time.sleep(delay_sec)
    os.chdir(repo_name)


    print("Creating g3d_update_temp folder to store .git, .gitignore and README.md...")
    time.sleep(delay_sec)
    os.mkdir("g3d_update_temp")
    shutil.copytree(".git", "g3d_update_temp/.git", dirs_exist_ok = True)
    shutil.move(".gitignore", "g3d_update_temp")
    shutil.move("README.md", "g3d_update_temp")

    print("Deleting all old files except the g3d_update_temp folder...")
    time.sleep(delay_sec)
    os.system(r"find . -mindepth 1 ! -regex '^./g3d_update_temp\(/.*\)?' -delete")

    print("Copying all the contents of the latest {} to Release/{}".format(repo_name, repo_name))
    shutil.copytree("../../{}".format(repo_name), os.getcwd(), dirs_exist_ok = True)

    print("Deleting old README.md...")
    print("Deleting old .git...")
    print("Deleting old .gitignore...")
    time.sleep(delay_sec)
    os.remove("README.md")
    shutil.rmtree(".git")
    os.remove(".gitignore")

    print("Copying latest README.md, .git and .gitignore from g3d_update_temp...")
    time.sleep(delay_sec)
    shutil.copytree("g3d_update_temp/.git", os.path.join(os.getcwd(), ".git"))
    shutil.copy("g3d_update_temp/.gitignore", os.getcwd())
    shutil.copy("g3d_update_temp/README.md", os.getcwd())

    print("Deleting g3d_update_temp...")
    time.sleep(delay_sec)
    shutil.rmtree("g3d_update_temp")

    print("Deleting all .cpp and .h files.")
    time.sleep(delay_sec)
    os.system('find . -name "*.cpp" -type f -delete')
    os.system('find . -name "*.h" -type f -delete')

    print()
    print("***************************************************************************")
    print("""
    CREATING UPDATE SUCCESS

    Please update the version in config manually.

    Zip the {} located at Release
    folder to have USB update to be tested before pushing it to GitHub OTA update.

    Once tested, you can push this to GitHub OTA manually.
    [The one located at Release/G3D-Printer-Release-master]
    > git add -A
    > git commit -m "Updated to Version xx.xx.xx"
    > git push origin master
    """.format(repo_name))
    print("***************************************************************************")







