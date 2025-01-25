import os
import json

from threading import Thread


from .. import console
from ..paths import PROJ_DIRS, MODIF_LOG_FILE
from ..config import get_proj_config, read_pc_file, Package
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

    logs = get_logs()    # Logs

    # Object files and src files
    o_files: dict = get_object_files()       # object files
    src_files: list[str] = get_src_files()   # source files

    if len(src_files) <= 0: 
        console.print("[err]Error[/err] -> Empty src directory.")
        return False

    # Options to provide while compiling and linking
    cflags: list[str] = []   # Compilation flags
    libs: list[str] = []     # Linker flags


    # Collect cflags and libs from all package config files
    for pc_file in os.scandir(PROJ_DIRS["DEBUG_LIB_PKGCONFIG_DIR"]):
        pkg: Package = read_pc_file(pc_file.path)
        if pkg:
            cflags.append(pkg.cflags.replace('\"', '').replace('${includedir}', PROJ_DIRS["INCLUDE_DIR"]))
            libs.append(pkg.libs.replace('\"', '').replace('${libdir}', PROJ_DIRS["DEBUG_LIB_DIR"]))


    # list containing threads of compile_src functions
    compile_queue: list[Thread] = []

    # Checks if error occurs while compilation
    compile_status: list[bool] = []

    # For all source files check if the file is newly created or modified.
    # newly created files will be compiled
    # and modified files will be re-compiled
    for src_path in src_files:

        # Get the last modified time stat
        file_last_modified = os.stat(src_path).st_mtime

        # hex encoded filename
        cache_file = src_path.encode('utf-8').hex() + '.o'
        
        # if cached file is not present in cache directory
        # or if it is modified
        if cache_file not in o_files or src_path in logs and logs[src_path] != file_last_modified:
            compile_queue.append(
                Thread(
                    target=compile_src, args=({
                        'logs': logs,
                        'file_last_modified': file_last_modified
                    }, src_path, cflags, compile_status, proj_config['debug']['Cflags'])
                )
            )

    # start compilation processes
    for process in compile_queue:
        process.start()

    # Checks if the source file for the compiled object exists.
    # if not then deletes the cached object file
    for o_file, o_file_path in o_files.items():
        file = bytes.fromhex(o_file.replace('.o', '')).decode('utf-8')
        if file not in src_files:
            os.remove(o_file_path)
    
    # Checks if file in log data exists if not then deletes that log
    for file in list(logs.keys()):
        if not os.path.exists(file):
            del logs[file]

    # wait for compilation to complete
    for process in compile_queue:
        process.join()

    # Update the log file
    update_logs(logs)

    # Link all the object files and create executable
    if False not in compile_status:
        zig_link(
            input_files=[*get_object_files().values()], 
            output_path=os.path.join(PROJ_DIRS["DEBUG_BIN_DIR"], proj_config['project']['name']),
            libs=libs,
            additional_flags=proj_config['debug']['Lflags']
        )
        return True
    return False

# Reads the log file and returns its contents
# @returns: dict of logs
def get_logs() -> dict:
    logs: dict = {}
    try:
        with open(MODIF_LOG_FILE, 'r') as f:
            logs = json.load(f)
    except FileNotFoundError:
        console.print(f"[err]Error[/err] [dim](while reading logs)[/dim] -> File '{MODIF_LOG_FILE}' not found.")
    except json.JSONDecodeError as e:
        console.print(f"[err]Error[/err] [dim](while reading logs)[/dim] -> Invalid JSON syntax in file '{MODIF_LOG_FILE}': {e}")
    except Exception as e:
        console.print(f"[err]Error[/err] -> {e}")
    return logs


# Ovveride the log file with new log_content
# @param log_content (dict): new log content
def update_logs(log_content: dict) -> None:
    with open(MODIF_LOG_FILE, 'w') as f:
        json.dump(log_content, f, indent=2)


# Compilation process function
# this will execute in thread
def compile_src(log_data: dict, src_path: str, cflags: list, compile_result: list[bool], additonal_flags: str = "") -> None: 
    if not zig_compile(src_path, cflags, additional_flags=additonal_flags): # compile the file
        compile_result.append(False)
        return
    
    log_data['logs'][src_path] = log_data['file_last_modified']
    compile_result.append(True)