
from rich.console import Console


console = Console()


def Print_Error(err: str):
    console.print('[ [bright_red]Error[/bright_red] ] ', err)

def Print_Warning(warn: str):
    console.print('[ [deep_pink2]Warning[/deep_pink2] ] ', warn)

def Print_Msg(label, msg: str, end: str = '\n'):
    console.print(f'[ [chartreuse1]{label}[/chartreuse1] ] ', msg, end=end)