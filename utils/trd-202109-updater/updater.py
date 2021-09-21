#!/usr/bin/env python3

import click
import errno
from loguru import logger
import os
import requests
import sys
import yaml


def parse_dump(x):
    top, body, status = "", "", ""
    if 'Win!' in x:
        status = "Win!"
        top, body = x.split("Win!")
    elif 'Lose! in x':
        status = "Lose!"
        top, body = x.split("Lose!")
    else:
        raise f"Unknown x data: {x}"
    elapsed_time = top.split()[0]
    return status, elapsed_time, body


def verify_dump(status, server, body):
    if status == 'Lose!':
        logger.info("Reported status is a lose, assuming this is accruate.")
        return True
    zeroth_cell = body.splitlines()[2].split()[0]
    maybe_flag_or_reveal = True if zeroth_cell[0] == '1' else False
    if maybe_flag_or_reveal:
        uri = f"{server}/flag/0/0"
    else:
        uri = f"{server}/reveal/0/0"
    logger.info("Making request to server to verify game status")
    logger.debug(f"POSTing to {uri}")
    r = requests.post(uri, data=body)
    if status in r.text:
        logger.info("Reported status verified by mineswepttd server.")
        return True
    else:
        logger.info("Reported status does not match mineswepttd server report.")
        return False


def create_configmap():
    base_cm = """
apiVersion: v1
kind: ConfigMap
metadata:
  name: ""
data: ""
"""
    return base_cm


def get_or_create_configmap(cm_path):
    file = ""
    try:
        with open(cm_path, 'r') as f:
            file = f.read()
    except OSError as e:
        if e.errno not in (errno.ENOENT, errno.ENOTDIR):
            raise e
        file = create_configmap()
    return yaml.safe_load(file)

def update_configmap(cm, author, run, status, time):
    if not cm['metadata']['name']:
        cm['metadata']['name'] = f"{author}-results"
    data = yaml.safe_load(cm.get('data', {}))
    data = data if data else {}
    data['runs'] = data.get('runs', [])
    runs = data['runs']
    runs.append({run: {'status': status, 'elapsed_time': time}})
    data['runs'] = runs
    cm['data'] = yaml.dump(data)
    return cm


def write_configmap(path, cm):
    with open(path, 'w') as f:
       f.write(yaml.dump(cm))

@click.command()
@click.option('--server')
@click.option('--author')
@click.option('--run')
@click.option('--configmap_path')
@click.option('--dump')
@logger.catch
def main(server, author, run, configmap_path, dump):
    logger.info("Beginning verification process...")
    logger.debug(f"Server: {server}, dump: {dump}")
    status, elapsed_time, body = parse_dump(dump)
    logger.debug(f"status: {status},",
                 f"elapsed_time: {elapsed_time},",
                 "body: {body}")
    verified = verify_dump(status, server, body)
    if not verified:
        logger.info("Updating status to match reality.")
        status = 'Win!' if status != 'Win!' else 'Lose!'
    logger.info("Updating or creating configmap")
    configmap = update_configmap(get_or_create_configmap(configmap_path),
                                 author, run, status, elapsed_time)
    logger.debug(configmap)
    logger.info(f"Writing updated configmap to {configmap_path}")
    write_configmap(configmap_path, configmap)



if __name__ == '__main__':
    main()
