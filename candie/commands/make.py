import json

from ..paths import *
from ..config import get_proj_config, read_package_config, Package
from ..utils import zig_compile, zig_link, get_object_files, get_src_files, check_valid_proj_and_zig_installed


# Makes an executable file
# compiles all source files and cache them
# links all the object files in to an executable
def make_app(verbose: bool = False) -> None:

    if not check_valid_proj_and_zig_installed():
        return

    proj_config = get_proj_config()

    old_log = get_logs()
    new_log: dict = {}


    o_files: list[str] = get_object_files()
    src_files: list[str] = get_src_files()

    cflags: list[str] = []
    libs: list[str] = []

    for pc_file in os.scandir(DIRS["DEBUG_LIB_PKGCONFIG_DIR"]):
        pkg: Package = read_package_config(pc_file.path)
        if pkg:
            cflags.append(pkg.cflags.replace('\"', '').replace('${includedir}', DIRS["INCLUDE_DIR"]))
            libs.append(pkg.libs.replace('\"', '').replace('${libdir}', DIRS["DEBUG_LIB_DIR"]))


    for src_path in src_files:

        file_path = str(src_path)
        file_last_modified = os.stat(src_path).st_mtime

        if not file_path.replace('/', '_') + '.o' in o_files:
            zig_compile(file_path, cflags)
        elif old_log[file_path] != file_last_modified:
            zig_compile(file_path, cflags)

        
        new_log[file_path] = file_last_modified


    update_logs(new_log)

    zig_link([*get_object_files().values()], os.path.join(DIRS["DEBUG_BIN_OUTPUT_DIR"], proj_config.name), libs, verbose=verbose)



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