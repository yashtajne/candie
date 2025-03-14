import os
import io
import re
import sys
import shutil
import json
import zipfile
import requests
import pkgconfig
import subprocess


from . import C, PROJECT, LOCAL_INSTALL_DIR, PROJECT_ROOT, NATIVE, DOWNLOADS_DIR, _GLOBAL_NAMESPACE_, parse, setup, execute
from .printer import Print_Error, Print_Msg


# Download a project from remote and builds it
def Fetch_Content(
        url: str,
        place: str = DOWNLOADS_DIR
    ):

    Print_Msg('Fetch', f'Remote {url}')
    os.makedirs(os.path.join(place, "dist"), exist_ok=True)

    with requests.get(url, stream=True) as response:
        if response.status_code == 200:
            content_disposition = response.headers.get("Content-Disposition")
            if content_disposition and "filename=" in content_disposition:
                zip_filename = content_disposition.split("filename=")[-1].strip('"')
            else:
                zip_filename = url.split("/")[-1]
            zip_path = os.path.join(place, "dist", zip_filename)

            # Writing stream
            with open(zip_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            #Unarchive zip file
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(place)

            # os.remove(zip_path)

            # Build file path
            buildfile = os.path.join((content_root := os.path.join(place, os.path.splitext(zip_filename)[0])), 'Candie.build')

            Print_Msg('Build', 'Starting installation')

            Print_Msg('Build', 'Switching PROJECT_ROOT')
            _GLOBAL_NAMESPACE_['PROJECT_ROOT'] = content_root

            sections = parse(buildfile)
            setup(sections)
            execute(sections, 'BUILD')

            Print_Msg('Build', 'Reverting PROJECT_ROOT')
            _GLOBAL_NAMESPACE_['PROJECT_ROOT'] = PROJECT_ROOT

        else:
            Print_Error(f"Failed to download. HTTP Status Code {response.status_code}")


def Run_Command(
        *cmd,
        directory: str = PROJECT_ROOT, 
        shell: bool = False, 
        capture_output: bool = False
    ) -> subprocess.CompletedProcess:
    try:
        result = subprocess.run(
            list(cmd),
            cwd=directory,
            shell=shell,
            capture_output=capture_output,
            text=True,
            check=True
        )
        return result
    except subprocess.CalledProcessError as e:
        Print_Error(f"Command failed with return code {e.returncode} {e.cmd}")
        raise SystemError


# Finds the pkgconfig file of the library and returns its values.
def Grab_Dependency(
        name: str,
        debug: bool = False,
        triplet: str = NATIVE,
        directory: str = None
    ) -> (dict | None):
    directory = os.path.join(LOCAL_INSTALL_DIR, triplet) if directory is None else directory
    os.environ['PKG_CONFIG_PATH'] = f'{directory}{'/debug' if debug else ''}/lib/pkgconfig'
    return {
        'name': name,
        'debug': debug,
        'cflags': pkgconfig.cflags(name),
        'libs': pkgconfig.libs(name)
    } if pkgconfig.exists(name) else None

# Returns a library name based on the type of library and operating system.
def Generate_Library_Name(library_name: str, library_type: str, os_triplet: str) -> str:
    os_triplet = os_triplet.lower()
    if "darwin" in os_triplet or "macos" in os_triplet:
        os_prefix = 'lib'
        if library_type == 'static':
            os_suffix = '.a'
        elif library_type == 'dynamic':
            os_suffix = '.dylib'
        else:
            raise ValueError('Unsupported library type')
    elif "windows" in os_triplet:
        os_prefix = ''
        if library_type == 'static':
            os_suffix = '.lib'
        elif library_type == 'dynamic':
            os_suffix = '.dll'
        else:
            raise ValueError('Unsupported library type')
    else:
        os_prefix = 'lib'
        if library_type == 'static':
            os_suffix = '.a'
        elif library_type == 'dynamic':
            os_suffix = '.so'
        else:
            raise ValueError('Unsupported library type')

    return f'{os_prefix}{library_name}{os_suffix}'

# Grabs the files files with the provided extension from a directory
def Grab_Files(directory_path: str, file_ext: str) -> tuple[str, ...]:  
    source_directory_path = os.path.abspath(os.path.join(_GLOBAL_NAMESPACE_.get('PROJECT_ROOT', PROJECT_ROOT), directory_path))
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

def Generate_PkgConfig_File(
        name: str,
        description: str,
        version: str,
        url: str,
        requires: list[str],
        libs: list[str],
        cflags: list[str],
        debug: bool = False
    ):
    return f'''
prefix=${{pcfiledir}}/../..{'/..' if debug else ''}
exec_prefix=${{prefix}}
includedir=${{prefix}}/include
libdir=${{prefix}}/{'debug/lib' if debug else 'lib'}

Name: {name}
Description: {description}
Version: {version}
URL: {url}

Libs: "-L${{libdir}}" {' '.join(libs)}
Requires: {' '.join(requires)}
Cflags: "-I${{includedir}}" {' '.join(cflags)}
'''