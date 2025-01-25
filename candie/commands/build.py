import os


from ..paths import PROJ_DIRS
from ..config import Package, get_proj_config, read_pc_file
from ..utils import zig_link, get_src_files, check_valid_proj_and_zig_installed


# Builds the project
def build_proj():

    if not check_valid_proj_and_zig_installed():
        return
    
    proj_config = get_proj_config()

    cflags: list[str] = []
    libs: list[str] = []

    for pc_file in os.scandir(PROJ_DIRS["DEBUG_LIB_PKGCONFIG_DIR"]):
        pkg: Package = read_pc_file(pc_file.path)
        if pkg:
            cflags.append(pkg.cflags.replace('\"', '').replace('${includedir}', PROJ_DIRS["INCLUDE_DIR"]))
            libs.append(pkg.libs.replace('\"', '').replace('${libdir}', PROJ_DIRS["DEBUG_LIB_DIR"]))

    
    for target in proj_config['build']['target']:
        zig_link(
            input_files=get_src_files(), 
            output_path=os.path.join(PROJ_DIRS["BUILD_DIR"], f'{proj_config['project']['name']}-{target['arch']}-{target['os']}'),
            cflags=cflags,
            libs=libs,
            target=f'{target['arch']}-{target['os']}',
            additional_flags=proj_config['build']['flags']
        )