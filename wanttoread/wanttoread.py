#!/usr/local/bin/python3
# pylint: disable=missing-function-docstring, missing-module-docstring

from urllib.request import Request, urlopen
import sys
import click
from trello import TrelloApi
import bs4

import config


def setup():
    trello = TrelloApi(config.TRELLO_APP_KEY)
    trello.set_token(config.TRELLO_USER_TOKEN)
    return trello


def parse_page(url):
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    except ValueError:
        print(f"Invalid URL: {url}")
        sys.exit()
    webpage = urlopen(req).read()
    return bs4.BeautifulSoup(webpage, features="html.parser")


def get_title(page_soup):
    return page_soup.title.text


def get_readtime_in_min(page_soup):
    webpage_text = page_soup.get_text()
    word_count = len(webpage_text.split())
    return word_count / config.READING_SPEED_PER_MIN


def create_card(title, url, time_to_read_in_min):
    name = f"[Read Article] ({time_to_read_in_min} minutes) {title}"
    trello.cards.new(idList=config.TRELLO_LIST_ID, name=name, desc=url)
    print(f"Card created: {name}")


@click.group()
def cli():
    pass


@click.argument("username")
@click.command()
def get_boards_list(username):
    boards_list = trello.members.get(username)["idBoards"]
    print("ID, Board Name")
    for board_id in boards_list:
        print(board_id, trello.boards.get(board_id)["name"])


@click.command()
@click.argument("board_id")
def get_lists_list(board_id):
    for trello_list in trello.boards.get_list(board_id):
        print(trello_list["id"], trello_list["name"])


@click.command()
@click.argument(
    "url"
)  # , default="https://www.leanproduction.com/theory-of-constraints.html", help='Number of greetings.')
def page(url):
    page_soup = parse_page(url)
    title = get_title(page_soup)
    readtime_in_min = get_readtime_in_min(page_soup)

    create_card(title, url, readtime_in_min)


cli.add_command(page)
cli.add_command(get_boards_list)
cli.add_command(get_lists_list)

if __name__ == "__main__":
    trello = setup()
    cli()
