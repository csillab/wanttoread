#!/usr/local/bin/python3
# pylint: disable=missing-function-docstring, missing-module-docstring

import click
from wanttoread import (
    wtr_get_boards_list,
    wtr_get_lists_list,
    wtr_page,
)

@click.group()
def cli():
    pass


@click.argument("username")
@click.command()
def get_boards_list(username):
    wtr_get_boards_list(username)


@click.command()
@click.argument("board_id")
def get_lists_list(board_id):
    wtr_get_lists_list(board_id)


@click.command()
@click.argument("url")
def page(url):
    wtr_page(url)

cli.add_command(page)
cli.add_command(get_boards_list)
cli.add_command(get_lists_list)

if __name__ == "__main__":
    cli()
