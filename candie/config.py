import platform
import toml


from .paths import *


class ProjectConfig():
    def __init__(self):
        self.name: str
        self.description: str
        self.version: str

        self.build: list[str]
        self.requirements: list[Package]


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

    config: dict = {}

    config["project"] = {
        "name": name,
        "description": description,
        "version": "0.0.1",
    }

    config["build"] = {
        "native": f'{platform.machine()}-{platform.system().lower()}'
    }

    with open(PROJ_CONFIG_FILE, 'w') as f:
        toml.dump(config, f)



# @returns: project config
def get_proj_config() -> ProjectConfig:

    config = ProjectConfig()

    with open(PROJ_CONFIG_FILE, 'r') as f:
        data = toml.load(f)

    config.name = data.get('project', {}).get('name')
    config.description = data.get('project', {}).get('description')
    config.version = data.get('project', {}).get('version')

    config.build = list(data.get('build', {}).values())
    config.requirements = data.get('requirements', [])

    return config


# Reads the <package>.pc file in the pkgconfig directory and returns the package object.
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
            
            package.name = os.path.basename(pc_file_path).removesuffix('.pc')

            return package
    except Exception as e:
        print(f"Error reading pc file: {e}")
        return None
