import os


from ..paths import *
from ..config import Package, get_proj_config, read_package_config
from ..utils import zig_link, get_src_files, check_valid_proj_and_zig_installed


# Builds the project
def build_proj():

    if not check_valid_proj_and_zig_installed():
        return
    
    proj_config = get_proj_config()

    cflags: list[str] = []
    libs: list[str] = []

    for pc_file in os.scandir(DIRS["DEBUG_LIB_PKGCONFIG_DIR"]):
        pkg: Package = read_package_config(pc_file.path)
        if pkg:
            cflags.append(pkg.cflags.replace('\"', '').replace('${includedir}', DIRS["INCLUDE_DIR"]))
            libs.append(pkg.libs.replace('\"', '').replace('${libdir}', DIRS["DEBUG_LIB_DIR"]))

    
    for target in proj_config.build:
        zig_link(
            input_files=get_src_files(), 
            output_path=os.path.join(DIRS["BUILD_DIR"], f'{proj_config.name}-{target}'),
            cflags=cflags,
            libs=libs,
            target=target
        )