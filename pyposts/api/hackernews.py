import click
import requests


@click.command("hnews", short_help="Get latest news from Hackernews")
def hnews() -> None:
    """
    Fetch the latest from HackerNews!
    """
    print("Working")
