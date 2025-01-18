import os
import subprocess


from .make import make_app
from ..paths import *
from ..config import get_proj_config


# Compiles the project and Runs the executable.
def run_prog(remake: bool) -> None:
    proj_config = get_proj_config()

    program = os.path.join(DIRS["DEBUG_BIN_OUTPUT_DIR"], proj_config.name)

    if remake:
        make_app()

    if os.path.exists(program):
        subprocess.run([program])