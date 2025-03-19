import typer
import importlib.metadata

from candie import parse, setup, execute

app = typer.Typer()


@app.command()
def x(
    s: str = typer.Argument(None, help="Execute a section."),
    v: bool = typer.Option(False, "--version", "-v", help="Show the version", is_eager=True)
) -> None:
    
    if v:
        typer.echo(f'''
candie (candie.kit) v{importlib.metadata.version('candie.kit')}
Copyright (C) 2025 Yash Tajne
This program may be freely redistributed under
the terms of the Apache Software License.
''')
        exit()    
    
    if s:
        sections = parse()
        setup(sections)
        execute(sections, s.upper())

def start() -> None:
    app()