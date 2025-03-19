import re
import os
import platform


class Arg(str):
    def __new__(cls, arg):
        obj = super().__new__(cls, arg)
        obj.value = arg
        return obj
    
class Target(str):
    def __new__(cls, cpu, os="", abi=""):
        if os and abi:
            triplet = f"{cpu}-{os}-{abi}"
        elif os:
            triplet = f"{cpu}-{os}"
        else:
            triplet = cpu
        obj = super().__new__(cls, triplet)
        return obj

_GLOBAL_NAMESPACE_ = globals()

PROJECT_ROOT = os.getcwd()
ARCHITECTURE = platform.architecture()
SYSTEM = platform.system()

# Files
CANDIEFILE = f"{PROJECT_ROOT}/Candiefile"

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
TARGETS = [
    (NATIVE := Target('native')),

    (X86_WINDOWS    := Target('x86',     'windows')),
    (X64_WINDOWS    := Target('x86_64',  'windows')),
    (ARM64_WINDOWS  := Target('aarch64', 'windows')),

    (X86_LINUX      := Target('x86',     'linux')),
    (X64_LINUX      := Target('x86_64',  'linux')),
    (ARM64_LINUX    := Target('aarch64', 'linux')),

    (ARM64_MACOS    := Target('aarch64', 'macos')),
    (X86_MACOS      := Target('x86',     'macos')),
    (X64_MACOS      := Target('x86_64',  'macos'))
]

# Compiler Args
C_ARGS = [

    # Optimization
    (O0 := Arg('-O0')),
    (O1 := Arg('-O1')),
    (O2 := Arg('-O2')),
    (O3 := Arg('-O3')),
    (OS := Arg('-Os')),
    (OZ := Arg('-Oz')),

    # Warning and error
    (W_ALL      := Arg('-Wall')),
    (W_EXTRA    := Arg('-Wextra')),
    (W_ERROR    := Arg('-Werror')),
    (W_PEDANTIC := Arg('-Wpedantic')),

    # Standard version c
    (STD_C89     := Arg('-std=c89')),
    (STD_C90     := Arg('-std=c90')),
    (STD_GNU89   := Arg('-std=gnu89')),
    (STD_C99     := Arg('-std=c99')),
    (STD_GNU99   := Arg('-std=gnu99')),
    (STD_C11     := Arg('-std=c11')),
    (STD_GNU11   := Arg('-std=gnu11')),
    (STD_C17     := Arg('-std=c17')),
    (STD_GNU17   := Arg('-std=gnu17')),
    (STD_C23     := Arg('-std=c23')),
    (STD_GNU23   := Arg('-std=gnu23')),

    # Standard version c++
    (STD_CPP98   := Arg('-std=c++98')),
    (STD_GNUPP98 := Arg('-std=gnu++98')),
    (STD_CPP03   := Arg('-std=c++03')),
    (STD_GNUPP03 := Arg('-std=gnu++03')),
    (STD_CPP11   := Arg('-std=c++11')),
    (STD_GNUPP11 := Arg('-std=gnu++11')),
    (STD_CPP014  := Arg('-std=c++14')),
    (STD_GNUPP14 := Arg('-std=gnu++14')),
    (STD_CPP17   := Arg('-std=c++17')),
    (STD_GNUPP17 := Arg('-std=gnu++17')),
    (STD_CPP20   := Arg('-std=c++20')),
    (STD_GNUPP20 := Arg('-std=gnu++20')),
    (STD_CPP23   := Arg('-std=c++23')),
    (STD_GNUPP23 := Arg('-std=gnu++23')),
]

# Linker arguments
LINK_ARGS = [

    # Optimiztion & Size reduction
    (WL_O1          := Arg('-Wl,-O1')),
    (WL_O2          := Arg('-Wl,-O2')),
    (WL_ASNEEDED    := Arg('-Wl,--as-needed')),
    (WL_GC_SECTIONS := Arg('-Wl,--gc-sections')),
    (WL_STRIP_ALL   := Arg('-Wl,--strip-all')),
    (WL_STRIP_DEBUG := Arg('-Wl,--strip-debug')),
    (WL_ICF_SAFE    := Arg('-Wl,--icf=safe')),

    # For Performance
    (WL_HASH_STYLE_GNU := Arg('-Wl,--hash-style=gnu')),
    (WL_NO_KEEP_MEMORY := Arg('-Wl,--no-keep-memory')),
    (WL_THREADS        := Arg('-Wl,--threads')),

    # Debugging & Profiling
    (WL_EXPORT_DYNAMIC := Arg('-Wl,--export-dynamic')),
    (WL_PRINT_MAP      := Arg('-Wl,--print-map')),
    (WL_VERBOSE        := Arg('-Wl,--verbose')),
    (WL_WARN_COMMON    := Arg('-Wl,--warn-common')),
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

executable       = Executable
library          = Library
package          = Package

def project(name: str, language: str, version: str = '1.0.0') -> None:
    PROJECT['name'] = name
    PROJECT['language'] = language
    PROJECT['version'] = version

    if language not in [C, CPP]:
        Print_Error("Invalid Language", language)

    PROJECT['compiler'] = Compiler(PROJECT['language'], CACHE_DIR)
