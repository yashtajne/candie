
from rich.console import Console
from rich.themes import Theme


theme = Theme({
    "err": "bold bright_red",       # standard error
    "plog": "bold bright_green",    # compilation started or finished
    "cerror": "bold deep_pink2",    # compilation error
    "lilog": "bold bright_cyan",    # linking log
    "hinfo": "steel_blue1",         
    "abort": "orange_red1",
    "sigint": "magenta2",
})

console = Console(theme=theme)