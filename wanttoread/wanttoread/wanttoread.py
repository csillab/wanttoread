#!/usr/local/bin/python3
# pylint: disable=missing-function-docstring, missing-module-docstring

import sys
from trello import TrelloApi
import bs4

import wanttoread.config as config
import requests


def authenticate():
    trello = TrelloApi(config.TRELLO_APP_KEY)
    trello.set_token(config.TRELLO_USER_TOKEN)
    return trello


def parse_page(url):
    r = requests.get(url=url)
    return bs4.BeautifulSoup(r.text, features="html.parser")


def get_title(page_soup):
    return page_soup.title.text

def get_readtime_in_min(page_soup):
    tags_to_remove = ["script", "style"]
    for undesired_tag in page_soup.find_all(tags_to_remove):
        undesired_tag.decompose()

    webpage_text = page_soup.get_text()
    word_count = len(webpage_text.split())
    return word_count / config.READING_SPEED_PER_MIN

def create_card(title, url, time_to_read_in_min, trello):
    name = f"[Read Article] ({time_to_read_in_min} minutes) {title}"
    trello.cards.new(idList=config.TRELLO_LIST_ID, name=name, desc=url)
    print(f"Card created: {name}")


def wtr_page(url):
    trello = authenticate()
    page_soup = parse_page(url)
    title = get_title(page_soup)
    readtime_in_min = get_readtime_in_min(page_soup)

    create_card(title, url, readtime_in_min, trello)

def wtr_get_lists_list(board_id):
    trello = authenticate()
    for trello_list in trello.boards.get_list(board_id):
        print(trello_list["id"], trello_list["name"])

def wtr_get_boards_list(username):
    trello = authenticate()
    boards_list = trello.members.get(username)["idBoards"]
    print("ID, Board Name")
    for board_id in boards_list:
        print(board_id, trello.boards.get(board_id)["name"])
