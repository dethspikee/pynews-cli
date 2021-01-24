from typing import Generator

import click
import requests
import bs4

from pyposts.exceptions import check_for_request_errors


@click.command("hnews", short_help="Get latest news from Hackernews")
@click.option("-v/--no-verbose",
              "verbose", default=False,
              help="Show URLs and # of comments")
def hnews(verbose: str) -> None:
    """
    Fetch the latest from HackerNews!
    """
    stories = fetch_news()
    if verbose:
        click.echo_via_pager(show_news_verbose(stories))
    else:
        click.echo_via_pager(show_news(stories))


def show_news(stories: bs4.element.ResultSet) -> Generator[str, None, None]:
    """
    Yield all posts
    """
    counter = 0
    for story in stories:
        counter += 1
        link = story.get("href", "")
        text = story.text.strip()
        header = "{:>2}: {:>5}\n".format(counter, text)
        yield header


def show_news_verbose(stories: bs4.element.ResultSet) -> Generator[str, None, None]:
    """
    Yield all posts, URLs and # of comments
    """
    counter = 0
    for story in stories:
        counter += 1
        link = story.get("href", "")
        text = story.text.strip()
        header = "{:>3}: {:>5}\n".format(counter, text)
        url = "URL: {:>10}\n\n".format(link)
        yield header
        yield url

@check_for_request_errors
def fetch_news() -> bs4.element.ResultSet:
    """
    Fetch all posts from hacker news.
    Return Result Set containing <a> elements
    """
    URL = "https://news.ycombinator.com/"
    response = requests.get(URL)
    page = bs4.BeautifulSoup(response.content, "html.parser")
    stories = page.find_all("a", class_="storylink")

    return stories
