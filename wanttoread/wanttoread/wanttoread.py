#!/usr/local/bin/python3
# pylint: disable=missing-function-docstring, missing-module-docstring

import sys
import yaml
from trello import TrelloApi
import bs4

import requests

def _get_config():
    with open("wanttoread/config.yaml") as file_handler:
        return yaml.load(file_handler, Loader=yaml.FullLoader)

def authenticate():
    config = _get_config()
    trello = TrelloApi(config["TRELLO_APP_KEY"])
    trello.set_token(config["TRELLO_USER_TOKEN"])
    return trello


def parse_page(url):
    r = requests.get(url=url)
    return bs4.BeautifulSoup(r.text, features="html.parser")


def get_title(page_soup):
    return page_soup.title.text

def get_readtime_in_min(page_soup, reading_speed_per_min):
    tags_to_remove = ["script", "style"]
    for undesired_tag in page_soup.find_all(tags_to_remove):
        undesired_tag.decompose()

    webpage_text = page_soup.get_text()
    word_count = len(webpage_text.split())
    return word_count / reading_speed_per_min

def create_card(title, url, time_to_read_in_min, trello, trello_list_id):
    name = f"[Read Article] ({time_to_read_in_min} minutes) {title}"
    trello.cards.new(idList=trello_list_id, name=name, desc=url)
    print(f"Card created: {name}")


def wtr_page(url):
    trello = authenticate()
    config = _get_config()
    page_soup = parse_page(url)
    title = get_title(page_soup)
    readtime_in_min = get_readtime_in_min(page_soup, config["READING_SPEED_PER_MIN"])

    create_card(title, url, readtime_in_min, trello, config["TRELLO_LIST_ID"])

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
