import requests
import click

import pyposts
from pyposts.api import hackernews


@click.group()
@click.version_option(version=pyposts.__version__)
def cli() -> None:
    """
    Fetch news directly from your shell
    """
    pass



cli.add_command(hackernews.hnews)

cli()
