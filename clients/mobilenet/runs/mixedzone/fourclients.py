import json
import logging
import sys
import time

import redis
from galileo.shell.shell import Galileo, init, Telemd, Experiment
from galileo.worker.context import Context

from clients.experiment.run import run
from clients.mobilenet.util import spawn_client_group


def main():
    params = {
        'service': {
            'image_url': 'https://i.imgur.com/0jx0gP8.png'
        }
    }
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as fd:
            params = json.load(fd)

    clients_groups = []
    logging.basicConfig(level=logging._nameToLevel['INFO'])
    try:
        ctx = Context()
        rds = ctx.create_redis()
        g = init(rds)
        telemd: Telemd = g['telemd']
        galileo: Galileo = g['g']
        print("discover workers:")
        print(galileo.discover())
        time.sleep(1)
        exp: Experiment = g['exp']

        zone_a_profile_paths = [
            './data/profiles/constant_rps_5_max_ia_1_period_1000_duration_20_delay_0.pkl',
            './data/profiles/constant_rps_5_max_ia_1_period_1000_duration_20_delay_10.pkl'
        ]

        zone_b_profile_paths = [
            './data/profiles/constant_rps_5_max_ia_1_period_1000_duration_20_delay_5.pkl',
            './data/profiles/constant_rps_5_max_ia_1_period_1000_duration_20_delay_10.pkl',
        ]

        image_url = params['service']['image_url']

        clients_groups.append(
            spawn_client_group(zone_a_profile_paths, 'zone-a', rds, galileo, image_url))
        clients_groups.append(
            spawn_client_group(zone_b_profile_paths, 'zone-b', rds, galileo,image_url))

        def requests():
            for idx, group in enumerate(clients_groups):
                if idx == len(clients_groups) - 1:
                    group.request(ia=('prerecorded', 'ran')).wait()
                else:
                    group.request(ia=('prerecorded', 'ran'))

        run(
            g=galileo,
            telemd=telemd,
            exp=exp,
            rds=rds,
            name=f'mobilenet-mixedzone-fourclients-{int(time.time())}',
            params=params,
            requests=requests
        )

    finally:
        for c in clients_groups:
            c.close()
        print('done')


def wait_keyspace(rds: redis.Redis):
    pubsub = rds.pubsub(ignore_subscribe_messages=True)
    pubsub.psubscribe('__keyspace@0__:*')
    while True:
        message = pubsub.get_message()
        if message is None:
            continue
        print(message)


if __name__ == '__main__':
    main()
