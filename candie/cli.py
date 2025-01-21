import typer


app = typer.Typer()



@app.command(help="Create a C/C++ project")
def create(project_name: str):
    from .commands.create import create_proj
    create_proj(project_name)


@app.command(help="Add a package to the project")
def add(package_name: str):
    from .commands.add import add_pkg
    add_pkg(package_name)


@app.command(help="Remove a package from the project")
def remove(package_name: str):
    from .commands.remove import remove_pkg
    remove_pkg(package_name)


@app.command(help="Make the debug application")
def make(verbose: bool = typer.Option(False, "--verbose", help="Be verbose")):
    from .commands.make import make_app
    make_app(verbose)


@app.command(help="Run the debug application")
def run(
    remake: bool = typer.Option(False, "--remake", help="Recompile and run the program"),
    show_metrics: bool = typer.Option(False, "--metrics", help="Prints usage metrics of the program")
):
    from .commands.run import run_prog
    run_prog(remake, show_metrics)


@app.command(help="Build the project")
def build():
    from .commands.build import build_proj
    build_proj()


@app.command(help="Print the version")
def version():
    print('version: 1.1.0')


def candie_exec():
    app()