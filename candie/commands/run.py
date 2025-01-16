import os
import subprocess


from ..paths import *
from ..config import get_proj_config


def run_prog():
    proj_config = get_proj_config()

    program = os.path.join(DIRS["DEBUG_BIN_OUTPUT_DIR"], proj_config.name)

    subprocess.run([program])