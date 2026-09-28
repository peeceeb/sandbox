"""Console script for langgraph."""

import typer
from rich.console import Console

from langgraph import utils

app = typer.Typer()
console = Console()


@app.command()
def main() -> None:
    """Console script for langgraph."""
    console.print("Replace this message by putting your code into langgraph.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    utils.do_something_useful()


if __name__ == "__main__":
    app()
