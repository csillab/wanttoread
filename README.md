# wanttoread

This is a small CLI tool that helps managing the articles I want to read. It will estimate the time
 for reading and places a new card in a pre-configured Trello list.

This tool is still in development phase. Absolutely no warranty.

I used Docker for development and testing.


## Configuration

In order to get the TRELLO_LIST_ID, where new cards should be created, please follow:

0. Start the container and attach to it:
```
docker-compose build
docker-compose run wanttoread
```

1. Edit the wattoread/config.py file and add the TRELLO_APP_KEY and TRELLO_USER_TOKEN. See https://trello.com/app-key for more details.
2. Get the board ID and list ID.
Get the board ID:
```
$ ./wanttoread.py get-boards-list [username]
ID, Board Name
board_id_xxxxxxxxxxxxxxx Test
```

Get the list ID:

```
$ ./wanttoread.py get-lists-list board_id_xxxxxxxxxxxxxxx
list_id_yyyyyyyyyyyyyyyy Inbox
```

3. Add the list ID to `wanttoread/config.py` as:
```
TRELLO_LIST_ID = "list_id_yyyyyyyyyyyyyyyy"
```

## Daily usage (for now)

```
docker-compose build
docker-compose run wanttoread
./wanttoread.py page https://www.leanproduction.com/theory-of-constraints.html
Card created: [Read Article] (24.16 minutes) Focus Improvement on the Manufacturing Constraint | Lean Production
```