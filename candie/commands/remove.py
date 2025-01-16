import os
import json
import toml
import shutil


from ..paths import *

# Removes all package files from the project directory
# @param package_name (str): name of the package
def remove_pkg(package_name: str) -> None:

    pkg_index_data: list[dict] = []

    if os.path.exists(PKG_INDEX_FILE):
        with open(PKG_INDEX_FILE, 'r') as f:
            pkg_index_data = json.load(f)

    pkg_to_remove: dict = None

    for pkg in pkg_index_data:
        for pkg_name in pkg.keys():
            if pkg_name == package_name:
                pkg_to_remove = pkg
            break

    if not pkg_to_remove:
        print(f"Package {package_name} is not added to this project.")
        return
        
    for pkg_dirs in pkg.values():
        for dir in pkg_dirs:
            for path in dir:
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)

    # pkg_index_data.remove(pkg)
    remove_pkg_from_requirements(package_name)

    with open(PKG_INDEX_FILE, 'w') as f:
        json.dump(pkg_index_data, f, indent=4)




# Removes the package from the requirements table in the project config
# @param: (str) Package name
def remove_pkg_from_requirements(package_name: str) -> None:

    with open(PROJ_CONFIG_FILE, "r") as f:
        data = toml.load(f)

    for pkg in data.get("requirements", {}).get("package", []):
        if pkg["name"] == package_name:
            data.setdefault("requirements", {}).setdefault("package", []).remove(pkg)

    with open(PROJ_CONFIG_FILE, "w") as f:
        toml.dump(data, f)