import platform
import configparser


from .paths import *



class Package:
    def __init__(self):
        self.name: str         = ''      # name of the package
        self.description: str  = ''      # package decription
        self.url: str          = ''      # package url
        self.version: str      = ''      # package version

        self.libs: str         = ''      # package libraries linking flags
        self.cflags: str       = ''      # compilation flags



# Creates project config file
# writes necessary values to the config file after creating it.
# @param name (str): name of the project
# @param description (str): project description
def create_proj_config_file(name: str, description: str = "") -> None:
    config = configparser.ConfigParser()

    config['Project'] = {
        'name': name,
        'description': description,
        'version': '0.0.1',
    }

    config['Build'] = {
        'native': f'{platform.machine()}-{platform.system().lower()}',
    }

    with open(PROJ_CONFIG_FILE, 'w') as proj_config_file:
        config.write(proj_config_file)



# @returns: project config
def get_proj_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(PROJ_CONFIG_FILE)
    return config


# Reads a package config file and returns the package object.
# @param pc_file_path (str): filepath of the .pc file
# @returns: Package or none if error occurs
def read_package_config(pc_file_path: str) -> Package|None:
    try:
        with open(pc_file_path, 'r') as file:
            package = Package()
            for line in file:
                line = line.strip()
                if not line or ":" not in line:
                    continue
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                if hasattr(package, key.lower()):
                    setattr(package, key.lower(), value)
            if not package.name:
                print("Error (not a package): package name not found in config file")
                return None
            return package
    except Exception as e:
        print(f"Error reading pc file: {e}")
        return None
