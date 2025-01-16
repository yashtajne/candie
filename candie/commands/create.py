import os

from rich.prompt import Prompt


from ..paths import *
from ..config import create_proj_config_file

# Creates a new project 
# with the given name
# @param project_name: str
def create_proj(project_name: str = '') -> None:

    if os.listdir(cwd):
        print("Error: Directory not empty!")
        return
    
    if project_name == '':
        project_name = Prompt.ask("Please enter Project Name")

    with open('.gitignore', 'w') as f:
            f.write('''
.candie/
build/
debug/
include/
lib/
''')
    
    for dir in DIRS.values():
        os.makedirs(dir, exist_ok=True)
    
    with open(os.path.join(DIRS["SRC_DIR"], 'main.c'), 'w') as f:
                f.write('''
#include<stdio.h>

int main() {
    printf("Hello, World!");
    return 0;
}
''')
    
    create_proj_config_file(project_name)

    with open(MODIF_LOG_FILE, 'w') as f:
        f.write('{}')

    print('Project created.')
    print('Run [candie make] to compile.\nThen run the program using [candie run] command')
