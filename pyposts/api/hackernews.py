from typing import Generator
from itertools import zip_longest

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
    if verbose:
        stories = fetch_news_verbose()
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


def show_news_verbose(posts: dict) -> Generator[str, None, None]:
    """
    Yield all posts, URLs and # of comments
    """
    counter = 0
    for post, data in posts.items():
        counter += 1
        comment, url = data
        header = "{:<3}: {:>5}\n".format(counter, post)
        url = "URL: {:>10}\n".format(url)
        comment = "{} comment(s)\n\n".format(comment)
        yield header
        yield url
        yield comment

@check_for_request_errors
def fetch_news_verbose() -> dict:
    """
    Fetch all posts and return posts, and
    # of comments
    """
    URL = "https://news.ycombinator.com/"
    response = requests.get(URL, timeout=10)
    page = bs4.BeautifulSoup(response.content, "html.parser")

    stories = page.find_all("a", class_="storylink")
    td_row = page.find_all("td", class_="subtext")
    a_tags = [a_tag.find_all("a")[-1] for a_tag in td_row]

    comments = [comment.text.split()[0] for comment in a_tags]
    comments = [comment if comment.isnumeric() else "No comments"
                for comment in comments]
    posts = [story.text for story in stories]
    links = [story.get("href", "") for story in stories]

    all_posts = {post: [comment, url] for (post, comment, url)
                 in zip_longest(posts, comments, links, fillvalue="missing")}


    return all_posts
