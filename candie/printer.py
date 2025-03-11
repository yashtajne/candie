
from rich.console import Console


console = Console()


def Print_Error(err: str):
    console.print('[ [bright_red]Error[/bright_red] ] ', err)


def Print_Warning(warn: str):
    console.print('[ [deep_pink2]Warning[/deep_pink2] ] ', warn)


def Log_Msg(msg: str):
    console.log('[ [chartreuse1]Msg[/chartreuse1] ] ', msg)