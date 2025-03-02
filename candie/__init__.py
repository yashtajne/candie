import re
import os
import io
import json
import toml
import pathlib
import platform

cwd = os.getcwd()
ARCHITECTURE = platform.architecture()
SYSTEM = platform.system()

# Files
CANDIEFILE = f"{cwd}/Candie.build"
LOGFILE = f"{cwd}/.candie/logfile.json"

# Directories
CANDIE_DIR = f"{cwd}/.candie"
CACHE_DIR = f"{cwd}/.candie/cache"
LOCAL_INSTALL_DIR = f"{CANDIE_DIR}/local"
VCPKG_INSTALL_DIR = f"{CANDIE_DIR}/external"

# Project data
PROJECT: dict = {}

# Languages
C:      str = '.c'
CPP:    str = '.cpp'

# Library types
STATIC = 'static'
SHARED = 'dynamic'


from .utils import (
    Grab_Files,
    Grab_Sources,
    Grab_Headers,
    Grab_Dependency
)

from .genrators import Executable, Package, Library
from .compiler import ZigToolchain as Compiler

grab_files       = Grab_Files
grab_sources     = Grab_Sources
grab_headers     = Grab_Headers
grab_dependency  = Grab_Dependency

compiler         = Compiler
executable       = Executable
library          = Library
package          = Package

from .printer import console

def project(name: str, language: str, version: str = '1.0.0') -> None:
    PROJECT['name'] = name
    PROJECT['language'] = language
    PROJECT['version'] = version

    PROJECT['compiler'] = Compiler(PROJECT['language'])

def parse(file: io.TextIOWrapper) -> dict:
    data = file.read()
    sections = re.findall(r'^\[(.*?)\](.*?)(?=^\[|\Z)', data, re.DOTALL | re.MULTILINE)
    parsed_data = {section.strip(): content.strip() for section, content in sections}
    return parsed_data

def setup() -> dict:
    if not os.path.isfile(CANDIEFILE):
        print("Error cannot find build instruction file")
        raise SystemExit
    
    for dir in [
        CANDIE_DIR,
        LOCAL_INSTALL_DIR,
        CACHE_DIR
    ]:
        if not os.path.isdir(dir):
            os.makedirs(dir)
    
    with open(CANDIEFILE, 'r') as f:
        sections = parse(f)
    
    exec(sections["SETUP"])
    del sections["SETUP"]
    
    # console.print("Sections:", sections)
    # console.print("Project:", PROJECT)
    
    return sections

def execute(section: str) -> None:
    sections = setup()
    exec(sections[section])