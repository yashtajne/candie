import typer


from candie import parse, setup, execute

app = typer.Typer()


@app.command()
def x(
    option: str
) -> None:
    sections = parse()
    setup(sections)
    execute(sections, option.upper())


def start() -> None:
    app()