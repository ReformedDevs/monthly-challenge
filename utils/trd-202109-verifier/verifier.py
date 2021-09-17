#!/usr/bin/env python3

import click
from loguru import logger
import requests
import sys


def parse_dump(x):
    top, body, status = "", "", ""
    if 'Win!' in x:
        status = "win"
        top, body = x.split("Win!")
        print(x.split("Win!"))
    elif 'Lose! in x':
        status = "lose"
        top, body = x.split("Lose!")
    else:
        raise f"Unknown x data: {x}"
    elapsed_time = top.split()[0]
    return status, elapsed_time, body


@click.command()
@click.option('--server')
@click.option('--dump')
@logger.catch
def main(server, dump):
    logger.info("Beginning verification process...")
    logger.debug(f"Server: {server}, dump: {dump}")
    status, elapsed_time, body = parse_dump(dump)
    logger.debug(f"status: {status},",
                 f"elapsed_time: {elapsed_time},",
                 "body: {body}")
    if status == 'lose':
        logger.info("Game losed. Sending results to stdout and exiting...")
        print(f"'elapsed_time: {elapsed_time}, 'status': 'Lose!'")
        sys.exit()
    zeroth_cell = body.splitlines()[2].split()[0]
    maybe_flag_or_reveal = True if zeroth_cell[0] == '1' else False
    if maybe_flag_or_reveal:
        uri = f"{server}/flag/0/0"
    else:
        uri = f"{server}/reveal/0/0"
    logger.info("Making request to server to verify game status")
    r = requests.post(uri, data=body)
    if 'Win!' in r.text:
        logger.info("Game won. Sending results to stdout and exiting...")
        print(f"'elapsed_time: {elapsed_time}, 'status': 'Win!'")
        sys.exit()
    else:
        logger.info("LIAR! You did not win!",
                    "You're a loser!",
                    "Sending results to stdout and exiting...")
        print(f"'elapsed_time: {elapsed_time}, 'status': 'Lose!'")
        sys.exit()



if __name__ == '__main__':
    main()
