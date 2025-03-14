import re
import os
import io
import platform

from rich import print

_GLOBAL_NAMESPACE_ = globals()

PROJECT_ROOT = os.getcwd()
ARCHITECTURE = platform.architecture()
SYSTEM = platform.system()

# Files
CANDIEFILE = f"{PROJECT_ROOT}/Candie.build"

# Directories
CANDIE_DIR = f"{PROJECT_ROOT}/.candie"
LOCAL_INSTALL_DIR = f"{CANDIE_DIR}/installed"
DOWNLOADS_DIR = f"{CANDIE_DIR}/downloads"
CACHE_DIR = f"{CANDIE_DIR}/cache"

# Project object
PROJECT: dict = {}

# Languages
C:      str = '.c'
CPP:    str = '.cpp'

# Library types
STATIC = 'static'
SHARED = 'dynamic'

# Triplets
# 32 bit ARM is not working for some reason :(
TRIPLETS = [
    (NATIVE := 'native'),

    (X86_WINDOWS    := 'x86-windows'),
    (X64_WINDOWS    := 'x86_64-windows'),
    # (ARM_WINDOWS  := 'arm-windows'),
    (ARM64_WINDOWS  := 'aarch64-windows'),

    (X86_LINUX      := 'x86-linux'),
    (X64_LINUX      := 'x86_64-linux'),
    # (ARM_LINUX    := 'arm-linux'),
    (ARM64_LINUX    := 'aarch64-linux'),

    # (ARM_MACOS    := 'arm-macos'),
    (ARM64_MACOS    := 'aarch64-macos'),
    (X86_MACOS      := 'x86-macos'),
    (X64_MACOS      := 'x86_64-macos')
]

# Compiler Args
C_ARGS = [

    # Optimization
    (O_0 := '-O0'),
    (O_1 := '-O1'),
    (O_2 := '-O2'),
    (O_3 := '-O3'),
    (O_S := '-Os'),
    (O_Z := '-Oz'),

    # Warning and error
    (W_ALL      := '-Wall'),
    (W_EXTRA    := '-Wextra'),
    (W_ERROR    := '-Werror'),
    (W_PEDANTIC := '-Wpedantic'),

    # Standard version c
    (STD_C89     := '-std=c89'),
    (STD_C90     := '-std=c90'),
    (STD_GNU89   := '-std=gnu89'),
    (STD_C99     := '-std=c99'),
    (STD_GNU99   := '-std=gnu99'),
    (STD_C11     := '-std=c11'),
    (STD_GNU11   := '-std=gnu11'),
    (STD_C17     := '-std=c17'),
    (STD_GNU17   := '-std=gnu17'),
    (STD_C23     := '-std=c23'),
    (STD_GNU23   := '-std=gnu23'),

    # Standard version c++
    (STD_CPP98   := '-std=c++98'),
    (STD_GNUPP98 := '-std=gnu++98'),
    (STD_CPP03   := '-std=c++03'),
    (STD_GNUPP03 := '-std=gnu++03'),
    (STD_CPP11   := '-std=c++11'),
    (STD_GNUPP11 := '-std=gnu++11'),
    (STD_CPP014  := '-std=c++14'),
    (STD_GNUPP14 := '-std=gnu++14'),
    (STD_CPP17   := '-std=c++17'),
    (STD_GNUPP17 := '-std=gnu++17'),
    (STD_CPP20   := '-std=c++20'),
    (STD_GNUPP20 := '-std=gnu++20'),
    (STD_CPP23   := '-std=c++23'),
    (STD_GNUPP23 := '-std=gnu++23'),
]



def parse(file: str = CANDIEFILE) -> dict:
    if not os.path.isfile(file):
        Print_Error("Build instruction file not found.")
        raise SystemExit

    with open(file, 'r') as f:
        data = f.read()
    sections = re.findall(r'^\[(.*?)\](.*?)(?=^\[|\Z)', data, re.DOTALL | re.MULTILINE)
    parsed_data = {section.strip(): content.strip() for section, content in sections}
    return parsed_data

def setup(sections: dict) -> None:
    
    for dir in [
        CANDIE_DIR,
        CACHE_DIR,
        LOCAL_INSTALL_DIR,
        DOWNLOADS_DIR
    ]:
        if not os.path.isdir(dir):
            os.makedirs(dir)
    
    exec(sections["SETUP"], _GLOBAL_NAMESPACE_)
    
    # console.print("Sections:", sections)
    # console.print("Project:", PROJECT)
    
def execute(sections: dict, option: str) -> None:
    exec(sections[option], _GLOBAL_NAMESPACE_)



from .utils import (
    Grab_Files,
    Grab_Sources,
    Grab_Headers,
    Grab_Dependency,

    Fetch_Content,
    Run_Command,
)

from .genrators import Executable, Package, Library
from .compiler import ZigToolchain as Compiler
from .printer import Print_Error

grab_files       = Grab_Files
grab_sources     = Grab_Sources
grab_headers     = Grab_Headers
grab_dependency  = Grab_Dependency
fetch_content    = Fetch_Content
run_command      = Run_Command

compiler         = Compiler
executable       = Executable
library          = Library
package          = Package

def project(name: str, language: str, version: str = '1.0.0') -> None:
    PROJECT['name'] = name
    PROJECT['language'] = language
    PROJECT['version'] = version
    PROJECT['compiler'] = Compiler(PROJECT['language'], CACHE_DIR)
