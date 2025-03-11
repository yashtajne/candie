import typer


from candie import execute

app = typer.Typer()


@app.command()
def x(
    sec: str
) -> None:            
    execute(sec.upper())


def start() -> None:
    app()