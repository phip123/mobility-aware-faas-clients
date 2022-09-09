import json
import logging
import sys
import time

import redis
from galileo.shell.shell import Galileo, init, Telemd, Experiment
from galileo.worker.context import Context

from clients.experiment.run import run
from clients.mobilenet.util import spawn_zone_group


def main():
    params = {
        'service': {
            'image_url': 'https://i.imgur.com/0jx0gP8.png'
        },
        'n': 20,
        'ia': 0.5
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

        image_url = params['service']['image_url']
        ia = float(params['ia'])
        n = float(params['n'])

        c_a = spawn_zone_group('zone-a', 1, galileo, image_url)
        c_b = spawn_zone_group('zone-b', 1, galileo, image_url)

        clients_groups = [c_a, c_b]

        def requests():
            c_a.request(ia=ia, n=n)
            c_b.request(ia=ia, n=n).wait()

        run(
            g=galileo,
            telemd=telemd,
            exp=exp,
            rds=rds,
            name=f'mobilenet-single-latency-{int(time.time())}',
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
