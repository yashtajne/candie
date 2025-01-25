import os


from .. import console
from ..paths import PROJ_DIRS, cwd, MODIF_LOG_FILE
from ..config import create_proj_config_file

# Creates a new project
# with the given name
# @param project_name: str
def create_cmd(name: str, its_package: bool) -> None:

    if os.listdir(cwd):
        console.print("[err]Error[/err] directory not empty!")
        return

    with open('.gitignore', 'w') as f:
            f.write('''
.candie/
build/
debug/
include/
lib/
package/
test/
''')

    create_proj(project_name=name)
    console.print("[bright_white]Project created.[/bright_white]")

    with open(MODIF_LOG_FILE, 'w') as f:
        f.write('{}')



def create_proj(project_name: str):
    create_proj_config_file(project_name)
    for dir in PROJ_DIRS.values():
        os.makedirs(dir, exist_ok=True)

    with open(os.path.join(PROJ_DIRS["SRC_DIR"], 'main.c'), 'w') as f:
        f.write('''
#include<stdio.h>

int main() {
    printf("Hello, World!");
    return 0;
}
''')


# def create_pkg(package_name: str):
#     create_pkg_config_file(package_name)
#     for dir in PKG_DIRS.values():
#         os.makedirs(dir, exist_ok=True)

#     with open(os.path.join(PKG_DIRS["PACKAGE_HEADERS_DIR"], f'{package_name}.h'), 'w') as f:
#         f.write(f'''
# #ifndef _{package_name.upper()}_H_
# #define _{package_name.upper()}_H_
                
# int add(int a, int b);

# #endif
# ''')

#     with open(os.path.join(PKG_DIRS["PACKAGE_DIR"], f'{package_name}.c'), 'w') as f:
#         f.write(f'''
# #include "HEADERS/{package_name}.h"

# int add(int a, int b) {{
#     return a + b;
# }}
# ''')

#     with open(os.path.join(PKG_DIRS["SRC_DIR"], 'main.c'), 'w') as f:
#         f.write(f'''
# #include<stdio.h>
# #include<{package_name}.h>

# int main() {{
#     printf("%d", add(5 + 5));
#     return 0;
# }}
# ''')