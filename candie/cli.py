import typer


app = typer.Typer()


@app.command(help="Create a C/C++ Project")
def create(
    name: str,
    # its_a_package: bool = typer.Option(False, "--package", help="Creates a package")
):
    from .commands.create import create_cmd
    create_cmd(name, False)


@app.command(help="Add a package to the project")
def add(package_name: str):
    from .commands.add import add_pkg
    add_pkg(package_name)


@app.command(help="Remove a package from the project")
def remove(package_name: str):
    from .commands.remove import remove_pkg
    remove_pkg(package_name)


@app.command(help="Make the debug application")
def make():
    from .commands.make import make_app
    make_app()


@app.command(help="Run the debug application")
def run(
    remake: bool = typer.Option(False, "--remake", help="Recompile and run the program"),
    show_metrics: bool = typer.Option(False, "--metrics", help="Show system resource utilization"),
):
    from .commands.run import run_prog
    run_prog(remake, show_metrics)


@app.command(help="Build the project")
def build():
    from .commands.build import build_proj
    build_proj()


@app.command(help="Print the version")
def version():
    print('version: 1.1.9')


def candie_exec():
    app()