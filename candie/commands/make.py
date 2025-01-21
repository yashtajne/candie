import json

from ..paths import *
from ..config import get_proj_config, read_package_config, Package
from ..utils import zig_compile, zig_link, get_object_files, get_src_files, check_valid_proj_and_zig_installed


# Makes an executable file
# compiles all source files and cache them
# links all the object files in to an executable
def make_app(verbose: bool = False) -> bool:

    # validate project and requirements
    if not check_valid_proj_and_zig_installed():
        return

    # Get project config
    proj_config = get_proj_config()

    error_occured: bool = False
    logs = get_logs()    # Logs

    # print(logs)

    # Object files and src files
    o_files: dict = get_object_files()       # object files
    src_files: list[str] = get_src_files()   # source files


    # Options to provide while compiling and linking
    cflags: list[str] = []   # Compilation flags
    libs: list[str] = []     # Linker flags


    # Collect cflags and libs from all package config files
    for pc_file in os.scandir(DIRS["DEBUG_LIB_PKGCONFIG_DIR"]):
        pkg: Package = read_package_config(pc_file.path)
        if pkg:
            cflags.append(pkg.cflags.replace('\"', '').replace('${includedir}', DIRS["INCLUDE_DIR"]))
            libs.append(pkg.libs.replace('\"', '').replace('${libdir}', DIRS["DEBUG_LIB_DIR"]))



    # For all source files check if the file is newly created or modified.
    # newly created files will be compiled
    # and modified files will be re-compiled
    for src_path in src_files:

        # Get the last modified time stat
        file_last_modified = os.stat(src_path).st_mtime

        # hex encoded filename
        cache_file = src_path.encode('utf-8').hex() + '.o'
        
        # if cached file is not present in cache directory
        if cache_file not in o_files:
            if not zig_compile(src_path, cflags): # compile the file
                error_occured = True
                break
        # if file is modified
        elif src_path in logs and logs[src_path] != file_last_modified:
            if not zig_compile(src_path, cflags): # compile the file
                error_occured = True
                break

        # update logs dict
        logs[src_path] = file_last_modified


    # Checks if the source file for the compiled object exists.
    # if not then deletes the cached object file
    for o_file, o_file_path in o_files.items():
        file = bytes.fromhex(o_file.replace('.o', '')).decode('utf-8')
        if file not in src_files:
            os.remove(o_file_path)


    # Update the log file
    update_logs(logs)

    # Link all the object files and create executable
    if not error_occured:
        zig_link([*get_object_files().values()], os.path.join(DIRS["DEBUG_BIN_OUTPUT_DIR"], proj_config.name), libs, verbose=verbose)
        return True

    return False

# Reads the log file and returns its contents
# @returns: dict of logs
def get_logs() -> dict:
    logs: dict = {}
    with open(MODIF_LOG_FILE, 'r') as f:
        logs = json.load(f)
    return logs

# Ovveride the log file with new log_content
# @param log_content (dict): new log content
def update_logs(log_content: dict) -> None:
    with open(MODIF_LOG_FILE, 'w') as f:
        json.dump(log_content, f, indent=2)