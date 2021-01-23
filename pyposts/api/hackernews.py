from typing import Generator

import click
import requests
from bs4 import BeautifulSoup as BS


@click.command("hnews", short_help="Get latest news from Hackernews")
def hnews() -> None:
    """
    Fetch the latest from HackerNews!
    """

    click.echo_via_pager(fetch_news())

def fetch_news() -> Generator[str, None, None]:
    """
    Display all posts from the given page
    """
    URL = "https://news.ycombinator.com/"
    response = requests.get(URL)

    page = BS(response.content, "html.parser")
    stories = page.find_all("a", class_="storylink")
    for story in stories:
        link = story.get("href", "")
        text = story.text.strip()
        yield text + "\n" * 2

