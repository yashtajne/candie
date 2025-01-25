import os
import psutil
import subprocess
import tkinter as tk

from .. import console 
from .make import make_app
from ..paths import PROJ_DIRS
from ..config import get_proj_config
from ..utils import check_valid_proj_and_zig_installed


# Compiles the project and Runs the executable.
def run_prog(remake: bool, show_metrics: bool = False) -> None:

    # validate project and requirements
    if not check_valid_proj_and_zig_installed():
        return

    # get project config
    proj_config = get_proj_config()

    # Create program path
    program = os.path.join(PROJ_DIRS["DEBUG_BIN_DIR"], proj_config['project']['name'])

    # Recompile if remake true
    if remake:
        if not make_app():
            return

    # If program exists then run
    if os.path.exists(program):
        if show_metrics:

            process = psutil.Popen([program])
            window = tk.Tk()
            window.geometry("480x360")
            window.resizable(False, False)

            stats = tk.Label(window, justify="left")
            stats.pack(anchor='w')

            try:
                while process.status() not in [psutil.STATUS_STOPPED, psutil.STATUS_ZOMBIE]:

                    stats.config(text=f"""
    Process Name: {process.name()}
    Process ID: {process.pid}

    CPU Usage: {process.cpu_percent()}%
    Memory Usage: {process.memory_percent():.2f}%
        [RSS]  {process.memory_info().rss / (1024 * 1024):.2f} MB
        [VMS]  {process.memory_info().vms / (1024 * 1024):.2f} MB
    
    Thread Count: {process.num_threads()}

    Read Bytes: {process.io_counters().read_bytes / (1024 * 1024):.2f} MB
    Write Bytes: {process.io_counters().write_bytes / (1024 * 1024):.2f} MB
""")

                    window.update_idletasks()
                    window.update()

            except KeyboardInterrupt:
                console.print("\nProcess Interrupted")
            except Exception as e:
                console.print("[err]Error occured[/err] ->", e)
            finally:
                window.quit()
                process.kill()
                
        else:
            subprocess.run([program])
    else:
        console.print("[err]Error[/err] -> Executable not found")