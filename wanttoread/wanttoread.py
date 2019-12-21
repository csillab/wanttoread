#!/usr/local/bin/python3

import bs4
import urllib.request

reading_speed_per_min = 200
url = "https://www.leanproduction.com/theory-of-constraints.html"

from urllib.request import Request, urlopen

req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()

soup = bs4.BeautifulSoup(webpage, features="html.parser")
webpage_text = soup.get_text()
word_count = len(webpage_text.split())
time_to_read_in_min = word_count/reading_speed_per_min

print(time_to_read_in_min)
