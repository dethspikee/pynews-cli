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
    stories, comments = fetch_news_and_extract()
    if verbose:
        click.echo_via_pager(show_news_verbose(stories, comments))
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


def show_news_verbose(stories: bs4.element.ResultSet, comments) -> Generator[str, None, None]:
    """
    Yield all posts, URLs and # of comments
    """
    counter = 0
    for story, comment in zip(stories, comments):
        counter += 1
        link = story.get("href", "")
        text = story.text.strip()
        comment = comment if comment.isnumeric() else "No comments"
        header = "{:<3}: {:>5}\n".format(counter, text)
        url = "URL: {:>10}\n".format(link)
        comment = "Comments: {}\n\n".format(comment)
        yield header
        yield url
        yield comment

@check_for_request_errors
def fetch_news_and_extract() -> bs4.element.ResultSet:
    """
    Fetch all posts and exract posts, urls and comments
    from hacker news. Return Result Set containing
    <a> elements
    """
    URL = "https://news.ycombinator.com/"
    response = requests.get(URL)
    page = bs4.BeautifulSoup(response.content, "html.parser")
    stories = page.find_all("a", class_="storylink")
    td_row = page.find_all("td", class_="subtext")
    a_tags = [a_tag.find_all("a")[-1] for a_tag in td_row]
    comments = [comment.text.split()[0] for comment in a_tags]

    return stories, comments
