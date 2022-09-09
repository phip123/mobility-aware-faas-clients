import base64
import time
from typing import List

import redis
from galileo.shell.shell import Galileo, ClientGroup

from clients.experiment.arrivalprofile import clear_list, read_and_save_profile


def spawn_zone_group(zone: str, clients: int, g: Galileo, wait_ms: int) -> ClientGroup:
    return spawn_group(g, clients, f'busy-{zone}', wait_ms=wait_ms, labels={'galileo_zone': zone})


def spawn_group(g: Galileo, clients: int, service_name: str, wait_ms: int, labels: dict = None):
    path = f'/function/busy'
    return g.spawn(service_name, clients,
                   parameters={'method': 'post', 'path': path, 'kwargs': {'data': str(wait_ms)}},
                   worker_labels=labels)


def spawn_client_group(profile_paths: List[str], zone: str, rds: redis.Redis, galileo: Galileo, wait_ms: int):
    c = spawn_zone_group(zone, len(profile_paths), galileo, wait_ms)
    time.sleep(1)
    for index, client in enumerate(c.clients):
        profile_path = profile_paths[index]
        clear_list(client.client_id, rds)
        read_and_save_profile(profile_path, client, rds)
    return c


def wait_keyspace(rds: redis.Redis):
    pubsub = rds.pubsub(ignore_subscribe_messages=True)
    pubsub.psubscribe('__keyspace@0__:*')
    while True:
        message = pubsub.get_message()
        if message is None:
            continue
        print(message)
