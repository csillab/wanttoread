#!/usr/local/bin/python3

import bs4
import urllib.request
import config
from pprint import pprint
from trello import TrelloApi


url = "https://www.leanproduction.com/theory-of-constraints.html"

def calculate_read_time(url):

	from urllib.request import Request, urlopen

	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()

	soup = bs4.BeautifulSoup(webpage, features="html.parser")
	title = soup.title.text
	webpage_text = soup.get_text()
	word_count = len(webpage_text.split())
	time_to_read_in_min = word_count/config.READING_SPEED_PER_MIN
	return title, time_to_read_in_min

def setup():
	trello = TrelloApi(config.TRELLO_APP_KEY)
	trello.set_token(config.USER_TOKEN)
	return trello

def get_board_list(trello, url, time_to_read_in_min):
	board_ids = trello.members.get("csillabessenyei")["idBoards"]
	return board_ids

def print_boards(trello, board_list):
	print("ID, Board Name")
	for b in board_list:
		print(b, trello.boards.get(b)["name"])


def get_lists_list(trello):
	for list in trello.boards.get_list(config.BOARD_ID):
		print(list["id"], list["name"])

def create_card(trello):
	name = f"[Read Article] ({time_to_read_in_min} minutes) {title}"
	trello.cards.new(idList=config.LIST_ID, name=name, desc=url)

title, time_to_read_in_min = calculate_read_time(url)

trello = setup()
board_list = get_board_list(trello, url, time_to_read_in_min)
# print_boards(trello, board_list)
# get_lists_list(trello)
create_card(trello)
