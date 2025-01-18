import os
import json
import pathlib
import subprocess



from .paths import *



# @return: the root directory of vcpkg
def get_vcpkg_root() -> str|Exception:
    vcpkg_root = os.environ.get('VCPKG_ROOT')
    if vcpkg_root is None:
        raise Exception('VCPKG_ROOT is not set')
    return vcpkg_root


# @returns: str cc or c++ based on the file extention
def get_compiler_type(file: str|list[str]) -> str:
    if isinstance(file, str):
        if pathlib.Path(file).suffix == '.c':
            return'cc'
        elif pathlib.Path(file).suffix == '.cpp':
            return 'c++'
    elif isinstance(file, list):
        has_cpp = (pathlib.Path(f).suffix == '.cpp' for f in file)
        return 'c++' if has_cpp else 'cc'


# Runs the zig compile command and compiles the file
# @param src_file (str): filepath of the source file
def zig_compile(src_file: str, cflags: list[str]) -> bool:
    print('Compiling: ', pathlib.Path(src_file).name)
    cmd = ['zig', get_compiler_type(src_file), '-c', *cflags, src_file, '-o', os.path.join(DIRS["DEBUG_BIN_CACHE_DIR"], src_file.encode('utf-8').hex() + '.o')]
    result = subprocess.run(cmd)
    
    if result.returncode != 0:
        return False
    return True


# Runs the zig command to create an executable
# @param input_files list[str]: 
# @param target str: target of platfrom for creating the executable
def zig_link(input_files: list[str], output_path: str, libs: list[str], cflags: list[str] = [], target: str = 'native', verbose: bool = False) -> None:
    print(f'Linking: {len(input_files)} objects | target={target}')
    cmd = ['zig', get_compiler_type(input_files), '-target', target, *input_files, *cflags, *libs, '-o', output_path]
    if verbose :
        print("Command:", *cmd)
    result = subprocess.run(" ".join(cmd), shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr)


# Checks if package exists in the pkg-index.json file.
# If it does then it checks if all the files in the pkg exists or not
# @param package_name (str): name of the package.
# @return: True if exists else False
def pkg_exists(package_name: str) -> bool:

    pkg_index_data: list[dict] = []

    if os.path.exists(PKG_INDEX_FILE):
        with open(PKG_INDEX_FILE, 'r') as f:
            pkg_index_data = json.load(f)

    for pkg in pkg_index_data:
        for pkg_name in pkg.keys():
            if pkg_name == package_name:
                for pkg_dirs in pkg.values():
                    for dir in pkg_dirs:
                        for file in dir:
                            if not os.path.exists(file):
                                return False
                    return True
            break

    return False

# Copies a directory from the source path to the destination path.
# @param src_dir (str): The source directory path.
# @param dest_dir (str): The destination directory path.
# @return: A list of the directories that were copied.
def copy_directory(src_dir, dest_dir) -> list[str]:
    import shutil

    copied_so_far: list[str] = []

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for root, _, files in os.walk(src_dir):
        rel_path = os.path.relpath(root, src_dir)

        dest_subdir = os.path.join(dest_dir, rel_path)
        if not os.path.exists(dest_subdir):
            os.makedirs(dest_subdir)
            copied_so_far.append(dest_subdir)

        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_subdir, file)
            shutil.copy2(src_file, dest_file)
            copied_so_far.append(dest_file)

    return copied_so_far




# Reads the debug/bin/cache directory and creates a list of .o (object) files
# Returns: The list of object file paths
def get_object_files() -> dict:

    o_files: dict = {}

    for file in pathlib.Path(DIRS["DEBUG_BIN_CACHE_DIR"]).iterdir():
        if file.is_file():
            if file.suffix == '.o':
                o_files[file.name] = str(file.absolute())

    return o_files


# Reads the /src directory and creates a list of .c and .cpp files
# Returns: The list of source file paths
def get_src_files() -> list[str]:

    src_files: list[str] = []

    for file in pathlib.Path(DIRS["SRC_DIR"]).rglob("*.c"):
        src_files.append(str(file.absolute()))

    for file in pathlib.Path(DIRS["SRC_DIR"]).rglob("*.cpp"):
        src_files.append(str(file.absolute()))

    return src_files



# Checks if the project directory contains the project config file and zig is installed
# Returns: True if project is valid and zig is installed else False
def check_valid_proj_and_zig_installed() -> bool:
    
    if not os.path.exists(PROJ_CONFIG_FILE):
        print("Project config file not found")    
        return False

    try:
        ver = subprocess.run(["zig", "version"], capture_output=True, text=True)
    except FileNotFoundError as e:
        print("Error: zig is not installed")
        return False
    else:
        return True