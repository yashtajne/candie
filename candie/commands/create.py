import os

from rich.prompt import Prompt


from ..paths import *
from ..config import create_proj_config_file

# Creates a new project 
# with the given name
# @param project_name: str
def create_proj(project_name: str = '') -> None:

    if os.listdir(cwd):
        print("[bold bright_red]Error[/bold bright_red]: Directory not empty!")
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

    print('[bold spring_green2]Project created.[/bold spring_green2]')
    print('Run [hot_pink][candie make][/hot_pink] to compile.\nExecute the program using [hot_pink][candie run][/hot_pink] command')
