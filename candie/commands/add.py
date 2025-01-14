
import os
import json

from ..utils import get_vcpkg_root, pkg_exists, copy_directory
from ..paths import *



# Adds the package to the project directory
# @param package_name (str): Name of the package
def add_pkg(package_name: str) -> None:
    
    if not os.path.exists(PROJ_CONFIG_FILE):
        print("Project configuration file not found.")
        return 

    if pkg_exists(package_name):
        print("Package already added!")
        return
    
    pkg_dir_path = get_installed_pkg_dir_path(package_name)
    
    if not pkg_dir_path:
        print("package not installed")
        return
    
    if not is_pkg_valid(pkg_dir_path):
        print("Not a valid package")
        return
    
    copy_pkg(package_name, pkg_dir_path) 
    print('Added ', package_name)


# Copies all the pacakge files like include and lib to the project directory path
# @param package_name (str): name of the package
# @param package_path (str): path of the package
def copy_pkg(package_name: str, package_path: str) -> None:

    dirs_to_copy = {
        "LIB_DIR": os.path.join(package_path, "lib"),
        "INCLUDE_DIR": os.path.join(package_path, "include"),
        "DEBUG_LIB_DIR": os.path.join(package_path, "debug/lib"),
    }

    copied_contents: list[str] = []

    for dest, src in dirs_to_copy.items():
        try:
            copied_contents.append(copy_directory(src, os.path.join(DIRS[dest])))
            if not copied_contents[-1]:
                raise Exception("Error while copying files")
        except Exception as e:
            print(f"Error while adding package: {e}")
            print("Reverting changes, Cleaning up...")
            for copied_dir in copied_contents:
                for file in copied_dir:
                    os.remove(file)
            return
        
    pkg_index_data: list[dict] = []

    if os.path.exists(PKG_INDEX_FILE):
        with open(PKG_INDEX_FILE, 'r') as f:
            pkg_index_data = json.load(f)

    pkg_index_data.append({package_name: copied_contents})
    with open(PKG_INDEX_FILE, 'w') as f:
        json.dump(pkg_index_data, f, indent=2)


# Scans vcpkg root directory and finds the package directory for given the package name
# @param package_name (str): name of the package
# @Returns: (str) package path if package is installed | None if not installed
def get_installed_pkg_dir_path(package_name: str) -> str|None:

    with os.scandir(os.path.join(get_vcpkg_root(), "packages")) as entries:
        for entry in entries:
            if entry.is_dir():
                pkg_name = entry.name.split("_")[0]
                if pkg_name == package_name:
                    return entry.path
                
    return None
            

# Checks if the package contains the necessery files and directories
# @returns: True if pkg is valid | False if pkg not valid
def is_pkg_valid(package_path: str) -> bool:
    is_valid: bool = True

    if not os.path.exists(os.path.join(package_path, "include")):
        is_valid = False
    if not os.path.exists(os.path.join(package_path, "debug")):
        is_valid = False
    if not os.path.exists(os.path.join(package_path, "lib")):
        is_valid = False

    return is_valid