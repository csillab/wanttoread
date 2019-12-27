#!/usr/local/bin/python3
# pylint: disable=missing-function-docstring, missing-module-docstring

import argparse

from urllib.request import Request, urlopen

import sys

from trello import TrelloApi

import bs4
import config


# url = "https://www.leanproduction.com/theory-of-constraints.html"

parser = argparse.ArgumentParser()
parser.add_argument("url", help="URL for website to read")
args = parser.parse_args()


def calculate_read_time():
    try:
        req = Request(args.url, headers={"User-Agent": "Mozilla/5.0"})
    except ValueError:
        print(f"Invalid URL: {args.url}")
        sys.exit()
    webpage = urlopen(req).read()

    soup = bs4.BeautifulSoup(webpage, features="html.parser")
    title = soup.title.text
    webpage_text = soup.get_text()
    word_count = len(webpage_text.split())
    time_to_read_in_min = word_count / config.READING_SPEED_PER_MIN
    return title, time_to_read_in_min


def setup():
    trello = TrelloApi(config.TRELLO_APP_KEY)
    trello.set_token(config.USER_TOKEN)
    return trello


def get_board_list(trello, time_to_read_in_min):
    board_ids = trello.members.get(config.USERNAME)["idBoards"]
    return board_ids


def print_boards(trello, board_list):
    print("ID, Board Name")
    for board_id in board_list:
        print(board_id, trello.boards.get(board_id)["name"])


def get_lists_list(trello):
    for trello_list in trello.boards.get_list(config.BOARD_ID):
        print(trello_list["id"], trello_list["name"])


def create_card(trello, title, time_to_read_in_min):
    name = f"[Read Article] ({time_to_read_in_min} minutes) {title}"
    trello.cards.new(idList=config.LIST_ID, name=name, desc=args.url)


def main():
    title, time_to_read_in_min = calculate_read_time()
    trello = setup()
    # board_list = get_board_list(trello, time_to_read_in_min)
    # print_boards(trello, board_list)
    # get_lists_list(trello)
    create_card(trello, title, time_to_read_in_min)


main()
