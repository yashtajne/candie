import os
import subprocess


from .make import make_app
from ..paths import *
from ..config import get_proj_config
from ..utils import check_valid_proj_and_zig_installed


# Compiles the project and Runs the executable.
def run_prog(remake: bool) -> None:

    # validate project and requirements
    if not check_valid_proj_and_zig_installed():
        return

    # get project config
    proj_config = get_proj_config()

    # Create program path
    program = os.path.join(DIRS["DEBUG_BIN_OUTPUT_DIR"], proj_config.name)

    # Recompile if remake true
    if remake:
        make_app()

    # If program exists then run
    if os.path.exists(program):
        subprocess.run([program])
    else: 
        print("please compile the project first.")