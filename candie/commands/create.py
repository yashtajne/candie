import os

from ..paths import *
from ..config import create_proj_config_file

# Creates a new project 
# with the given name
# @param project_name: str
def create_proj(project_name: str) -> None:

    if os.listdir(cwd):
        print("Directory not empty!")
        return
    
    create_proj_config_file(project_name)

    for dir in DIRS.values():
        os.makedirs(dir, exist_ok=True)

    with open(MODIF_LOG_FILE, 'w') as f:
        f.write('{}')
