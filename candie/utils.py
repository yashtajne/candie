import os
import io
import re
import sys
import shutil
import json
import pkgconfig


from . import C, PROJECT, LOGFILE, LOCAL_INSTALL_DIR



def Get_Logs() -> dict:
    try:
        if not os.path.exists(LOGFILE):
            with open(LOGFILE, 'w') as logfile:
                json.dump({}, logfile)
        with open(LOGFILE, 'r') as logfile:
            logs = json.load(logfile)
        return logs
    except json.JSONDecodeError:
        pass

def Update_Logs(logs: dict) -> None:
    try:
        with open(LOGFILE, 'w') as logfile:
            json.dump(logs, logfile, indent=2)
    except Exception:
        pass

# Encode hex
def HEX_Encode(string: str):
    return string.encode('utf-8').hex()

# Decode hex 
def HEX_Decode(string: str):
    return bytes.fromhex(string).decode('utf-8')

# Finds the pkgconfig file of the library and returns its values.
def Grab_Dependency(
        library_name: str,
        debug: bool = False,
        dependency_dir: str = None
    ) -> (dict | None):
    dependency_dir = LOCAL_INSTALL_DIR if dependency_dir is None else dependency_dir
    os.environ['PKG_CONFIG_PATH'] = f'{dependency_dir}{'/debug' if debug else ''}/lib/pkgconfig'
    return {
        'name': library_name,
        'debug': debug,
        'cflags': pkgconfig.cflags(library_name),
        'libs': pkgconfig.libs(library_name)
    } if pkgconfig.exists(library_name) else None

# Returns a library name based on the type os library and operating system.
def Generate_Library_Name(library_name: str, library_type: str) -> str:
    if sys.platform.startswith('linux'):
        os_prefix = 'lib'
        if library_type == 'static':
            os_suffix = '.a'
        elif library_type == 'dynamic':
            os_suffix = '.so'
        else:
            raise ValueError('Unsupported library type')
    elif sys.platform.startswith('darwin'):
        os_prefix = 'lib'
        if library_type == 'static':
            os_suffix = '.a'
        elif library_type == 'dynamic':
            os_suffix = '.dylib'
        else:
            raise ValueError('Unsupported library type')
    elif sys.platform.startswith('win'):
        os_prefix = ''
        if library_type == 'static':
            os_suffix = '.lib'
        elif library_type == 'dynamic':
            os_suffix = '.dll'
        else:
            raise ValueError('Unsupported library type')
    else:
        raise ValueError('Unsupported operating system')

    library_name = f'{os_prefix}{library_name}{os_suffix}'
    return library_name

# Checks if package is installed
def Check_Package_Installed(package_name: str) -> bool:
    vcpkg_info_dir = './.candie/packages/vcpkg/info'
    if  os.path.isdir(vcpkg_info_dir):
        if package_name in (p.split('_')[0] for p in os.listdir(vcpkg_info_dir)):
            return True
    return False

# Grabs the files files with the provided extension from a directory
def Grab_Files(directory_path: str, file_ext: str) -> tuple[str, ...]:  
    source_directory_path = os.path.abspath(directory_path)
    return tuple(
        str(file.path) for file in os.scandir(source_directory_path) 
        if file.is_file() and file.name.endswith(file_ext)
    )

# Grabs the source (.c , .cpp) files from the specified directory
def Grab_Sources(source_directory_path: str) -> tuple[str, ...]:
    if PROJECT['language'] == C:
        return Grab_Files(source_directory_path, '.c')
    else:
        return Grab_Files(source_directory_path, '.c') + Grab_Files(source_directory_path, '.cpp')

# Grabs the header (.h, .hpp) files from the specified directory
def Grab_Headers(source_directory_path: str) -> tuple[str, ...]:
    if PROJECT['language'] == C:
        return Grab_Files(source_directory_path, '.h')
    else:
        return Grab_Files(source_directory_path, '.h') + Grab_Files(source_directory_path, '.hpp')

# Copies directory files from source to destination direcory
def Copy_Directory(src_dir, dest_dir) -> list[str]:
    copied: list[str] = []
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    for root, _, files in os.walk(src_dir):
        rel_path = os.path.relpath(root, src_dir)
        dest_subdir = os.path.join(dest_dir, rel_path)
        if not os.path.exists(dest_subdir):
            os.makedirs(dest_subdir)
            copied.append(dest_subdir)
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_subdir, file)
            shutil.copy2(src_file, dest_file)
            copied.append(dest_file)
    return copied

# Copy pastes files.
def Copy_Files(file_paths, destination_dir: str):
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        destination_file_path = os.path.join(destination_dir, file_name)
        try:
            shutil.copy(file_path, destination_file_path)
            print(f"Copied {file_path} to {destination_file_path}")
        except Exception as e:
            print(f"Error copying {file_path}: {str(e)}")

# Removes Cached files that are not being used
def Remove_Invalid_Cache(cache_dir: str) -> None:
    for root, dirs, files in os.walk(cache_dir):
        for file in files:
            try:
                source_file = bytes.fromhex(file[:-2]).decode('utf-8')
                if not os.path.exists(source_file):
                    os.remove(os.path.join(root, file))
            except ValueError:
                os.remove(os.path.join(root, file))
        for dir in dirs:
            if not os.path.isdir(HEX_Decode(dir)):
                shutil.rmtree(os.path.join(root, dir))

def Generate_PkgConfig_File(
        name: str,
        description: str,
        version: str,
        url: str,
        requires: list[str],
        libs: list[str],
        cflags: list[str]        
    ):
    return f'''
prefix=${{pcfiledir}}/../..
exec_prefix=${{prefix}}
includedir=${{prefix}}/include
libdir=${{prefix}}/lib

Name: {name}
Description: {description}
Version: {version}
URL: {url}

Libs: "-L${{libdir}}" {' '.join(libs)}
Requires: {' '.join(requires)}
Cflags: "-I${{includedir}}" {' '.join(cflags)}
'''