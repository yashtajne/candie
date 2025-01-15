import os

from rich.prompt import Prompt, Confirm


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

    project_description = Prompt.ask("Please enter Project Description")

    if Confirm.ask("Would you like me to add a .gitignore file?"):
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

    if Confirm.ask("Would you like me to add a main.c/cpp file to the project?"):
        file_choice = Prompt.ask("Which file should i create?\n 1: main.c\n 2: main.cpp", choices=['1', '2'])
        if file_choice == '1':
            with open(os.path.join(DIRS["SRC_DIR"], 'main.c'), 'w') as f:
                f.write('''
#include<stdio.h>

int main() {
    printf("Hello, World!");
    return 0;
}
''')
        else:            
            with open(os.path.join(DIRS["SRC_DIR"], 'main.cpp'), 'w') as f:
                f.write('''
#include<iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
''')
    
    create_proj_config_file(project_name, project_description)

    with open(MODIF_LOG_FILE, 'w') as f:
        f.write('{}')


    print('Project created.')
    print('Now, run [candie make] to compile.\nThen run the program using [candie run] command')
