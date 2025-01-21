import os
import time
import psutil
import subprocess

from rich.console import Console
from rich.panel import Panel

console = Console()

from .make import make_app
from ..paths import *
from ..config import get_proj_config
from ..utils import check_valid_proj_and_zig_installed


# Compiles the project and Runs the executable.
def run_prog(remake: bool, show_metrics: bool) -> None:

    # validate project and requirements
    if not check_valid_proj_and_zig_installed():
        return

    # get project config
    proj_config = get_proj_config()

    # Create program path
    program = os.path.join(DIRS["DEBUG_BIN_OUTPUT_DIR"], proj_config.name)

    # Recompile if remake true
    if remake:
        if not make_app():
            return

    # If program exists then run
    if os.path.exists(program):
        sub_process = subprocess.Popen([program])
        if show_metrics:
            process = psutil.Process(sub_process.pid)
            try:
                with console.status("Process Metrics") as status:
                    while True:
                        try:
                            if process.status() in (psutil.STATUS_DEAD, psutil.STATUS_ZOMBIE):
                                break

                            metrics = ''
                            metrics += f"[bold]CPU Usage:[/bold] {process.cpu_percent()}%\n"
                            metrics += f"[bold]Memory Usage:[/bold]\n"
                            metrics += f"  [blue]RSS:[/blue] {(process.memory_info().rss / (1024 * 1024)):.2f} MB\n"
                            metrics += f"  [blue]VMS:[/blue] {(process.memory_info().vms / (1024 * 1024)):.2f} MB\n"
                            metrics += f"[bold]Process Info:[/bold]\n"
                            metrics += f"  [blue]Thread Count:[/blue] {process.num_threads()}\n"
                            metrics += f"  [blue]Open Files:[/blue] {len(process.open_files())}\n"
                            metrics += f"[bold]I/O Metrics:[/bold]\n"
                            metrics += f"  [blue]Read Bytes:[/blue] {(process.io_counters().read_bytes / (1024 * 1024)):.2f} MB\n"
                            metrics += f"  [blue]Write Bytes:[/blue] {(process.io_counters().write_bytes / (1024 * 1024)):.2f} MB\n"
                            metrics += f"[bold]Network Metrics:[/bold]\n"
                            metrics += f"  [blue]Bytes Sent:[/blue] {(process.io_counters().write_bytes / (1024 * 1024)):.2f} MB\n"
                            metrics += f"  [blue]Bytes Received:[/blue] {(process.io_counters().read_bytes / (1024 * 1024)):.2f} MB\n"
                            metrics += f"[bold]Disk Metrics:[/bold]\n"
                            metrics += f"  [blue]Read Bytes:[/blue] {(process.io_counters().read_bytes / (1024 * 1024)):.2f} MB\n"
                            metrics += f"  [blue]Write Bytes:[/blue] {(process.io_counters().write_bytes / (1024 * 1024)):.2f} MB\n"
                            metrics += f"[bold]Other Metrics:[/bold]\n"
                            metrics += f"  [blue]Context Switches:[/blue] {process.num_ctx_switches()}\n"
                            metrics += f"  [blue]Handles:[/blue] {process.num_fds()}\n"

                            panel = Panel(metrics, title="Process Metrics")
                            status.update(panel)

                            time.sleep(0.5)
                        except psutil.AccessDenied:
                            console.print("Access denied. Cannot access process details.")
                            break
                        except psutil.NoSuchProcess:
                            console.print("Process does not exist.")
                            break
            except KeyboardInterrupt:
                console.print("\nProcess interrupted by user.")                
            finally:
                console.print("\nProcess has stopped running.")
    else: 
        print("please compile the project first.")