import click
from loguru import logger
import requests

@click.command()
@click.option('--server')
@click.option('--width')
@click.option('--height')
@click.option('--difficulty')
@click.option('--seed')
@logger.catch
def main(server, width, height, difficulty, seed):
    logger.debug(server, width, height, difficulty, seed)
    logger.debug(f"server: {server}, width: {width}, height: {height}, difficulty: {difficulty}, seed: {seed}")
    uri = f"{server}/new/{width}/{height}/{difficulty}?{seed}"
    logger.info(f"Making request to {uri}")
    r = requests.get(uri)
    b = r.text
    logger.info("Response returned.")
    logger.debug(f"Response Status: {r}")
    logger.debug(f"Response Body: {b}")
    logger.debug(f"Response Body: {b}")
    uri = f"{server}/flag/0/0?send_state=true"
    logger.info(f"Flagging the only cell, POSTing to '{uri}', expecting a winning result.")
    r = requests.post(uri, data=b)
    b = r.text
    logger.debug(f"Response Status: {r}")
    logger.debug(f"Response Body: {b}")
    logger.debug(f"Response Body: {b}")
    logger.info("Sending results and a madeup time to stdout")
    print(f"123.45 {b}")
    logger.info("Exiting. Good-bye.")



if __name__ == '__main__':
    main()
