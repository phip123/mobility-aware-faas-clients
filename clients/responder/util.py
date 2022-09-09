import time
from typing import List

import redis
from galileo.shell.shell import Galileo, ClientGroup

from clients.experiment.arrivalprofile import clear_list, read_and_save_profile


def spawn_zone_group(zone: str, clients: int, duration: int, g: Galileo, distribution: str = 'static',
                     cores=0) -> ClientGroup:
    return spawn_group(g, clients, duration, f'responder-{zone}', {'galileo_zone': zone}, distribution=distribution,
                       cores=cores)


def spawn_group(g: Galileo, clients: int, duration: int, service_name: str = 'nginx', labels: dict = None,
                distribution: str = 'static', cores: int = 0) -> ClientGroup:
    path = f'/function/request_responder_250/{distribution}?time={duration}&cores={cores}'
    return g.spawn(service_name, clients,
                   parameters={'method': 'get', 'path': path},
                   worker_labels=labels)


def spawn_client_group(profile_paths: List[str], zone: str, duration: int, rds: redis.Redis, galileo: Galileo,
                       distribution: str = 'static', cores=0):
    c = spawn_zone_group(zone, len(profile_paths), duration, galileo, distribution, cores)
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
