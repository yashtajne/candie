import os
import time
import psutil
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

    if os.path.exists(program):

        process = psutil.Popen([program])

        window = tk.Tk()
        window.geometry("480x360")
        window.resizable(False, False)

        stats = tk.Label(window, justify="left")
        stats.pack(anchor='w')

        if show_metrics:
            try:

                CPU_limit = proj_config["debug"]["limit"]["cpu"]
                RAM_limit = proj_config["debug"]["limit"]["ram"]
                Thread_limit = proj_config["debug"]["limit"]["thread"]

                while process.status() not in [psutil.STATUS_STOPPED, psutil.STATUS_ZOMBIE, psutil.STATUS_DEAD]:
                    
                    cpu_percent = process.cpu_percent()

                    mem_info = process.memory_info()
                    rss = mem_info.rss / (1024 * 1024) # in MB

                    threads = process.num_threads()

                    if cpu_percent > CPU_limit and CPU_limit != 0 :
                        console.print("\n[abort]CPU limit exceeded[/abort]")
                        break
                    elif rss > RAM_limit and RAM_limit != 0 :
                        console.print("\n[abort]RAM limit exceeded[/abort]")
                        break
                    elif threads > Thread_limit and Thread_limit != 0 :
                        console.print("\n[abort]Thread limit exceeded[/abort]")
                        break

                    time.sleep(0.5)

                    stats.config(text=f"""
    Process Name: {process.name()}
    Process ID: {process.pid}

    CPU Usage: {cpu_percent}%
    Memory Usage: {process.memory_percent():.2f}%
        [RSS]  {rss:.2f} MB
        [VMS]  {process.memory_info().vms / (1024 * 1024):.2f} MB
    
    Thread Count: {threads}

    Read Bytes: {process.io_counters().read_bytes / (1024 * 1024):.2f} MB
    Write Bytes: {process.io_counters().write_bytes / (1024 * 1024):.2f} MB
""")

                    window.update_idletasks()
                    window.update()

            except KeyboardInterrupt:
                console.print("\n[sigint]User Interrupt[/sigint]")
            except Exception as e:
                console.print("[err]Error occured[/err] ->", e)
            finally:
                process.kill()
                window.quit()
                console.print("[sigint]Process Terminated[/sigint]")
    else:
        console.print("[err]Error[/err] -> Executable not found")