import click

import pynews
from pynews.api import hackernews


@click.group()
@click.version_option(version=pynews.__version__)
def cli() -> None:
    """
    Fetch news directly from your shell
    """
    pass


cli.add_command(hackernews.hnews)
