import toml
import platform


from . import console
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
def create_proj_config_file(name: str) -> None:

    config: dict = {}

    config["project"] = {
        "name": name,
        "description": "",
        "version": "0.0.1",
    }

    config["debug"] = {
        'limit': {
            "cpu": 0,
            "ram": 0,
            "thread": 0,
        },
        'Cflags': ["-Wall", "-Wextra", "-g"],
        'Lflags': ["-Wl,--no-undefined"]
    }

    config["build"] = {
        'flags': ["-Wl,--no-undefined"],
        'target': [
            {
                'arch': platform.machine(),
                'os': platform.system().lower()
            }
        ]
    }

    with open(PROJ_CONFIG_FILE, 'w') as f:
        toml.dump(config, f)

# @returns: project config
def get_proj_config() -> dict:
    with open(PROJ_CONFIG_FILE, 'r') as f:
        config = toml.load(f)

    return {
        "project": {
            "name": config.get('project', {}).get('name', 'a'),
            "description": config.get('project', {}).get('description', ""),
            "version": config.get('project', {}).get('version', '0.0.0'),
        },
        "debug": {
            "limit": {
                "cpu": config.get('debug', {}).get('limit', {}).get('cpu', 0),
                "ram": config.get('debug', {}).get('limit', {}).get('ram', 0),
                "thread": config.get('debug', {}).get('limit', {}).get('thread', 0),
            }, 
            "Cflags": config.get('debug', {}).get('Cflags', []),
            "Lflags": config.get('debug', {}).get('Lflags', [])
        },
        "build": {
            "flags": config.get('build', {}).get('flags', []),
            "target": config.get('build', {}).get('target', [])
        },
        "requirements": {
            "package": config.get('requirements', {}).get('package', [])
        }
    }




# Reads the <package>.pc file in the pkgconfig directory and returns the package object.
# @param pc_file_path (str): filepath of the .pc file
# @returns: Package or none if error occurs
def read_pc_file(pc_file_path: str) -> Package|None:
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
                console.print("[err]Error[/err] [dim](not a package)[/dim] -> Package name not found in config file")
                return None
            
            package.name = os.path.basename(pc_file_path).removesuffix('.pc')

            return package
    except Exception as e:
        console.print(f"[err]Error[/err] [dim](while reading {pc_file_path} file)[/dim] -> {e}")
        return None
