import os


from ..paths import *
from ..config import Package, get_proj_config, read_package_config
from ..utils import zig_link, get_src_files


# Builds the project
def build_proj():

    if not os.path.exists(PROJ_CONFIG_FILE):
        print("Project configuration file not found.")
        return
    
    proj_config = get_proj_config()


    cflags: list[str] = []
    libs: list[str] = []

    for pc_file in os.scandir(DIRS["DEBUG_LIB_PKGCONFIG_DIR"]):
        pkg: Package = read_package_config(pc_file.path)
        if pkg:
            cflags.append(pkg.cflags.replace('\"', '').replace('${includedir}', DIRS["INCLUDE_DIR"]))
            libs.append(pkg.libs.replace('\"', '').replace('${libdir}', DIRS["DEBUG_LIB_DIR"]))

    
    for _, target in proj_config.items('Build'):
        zig_link(
            input_files=get_src_files(), 
            output_path=os.path.join(DIRS["BUILD_DIR"], f'{proj_config.get('Project', 'name')}-{target}'),
            cflags=cflags,
            libs=libs,
            target=target
        )