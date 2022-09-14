import time

import redis
from galileo.shell.shell import Galileo, init, Telemd, ClientGroup, Experiment
from galileo.worker.context import Context

from clients.experiment.arrivalprofile import read_and_save_profile, clear_list
from clients.experiment.run import run


def spawn_zone_group(zone: str, g: Galileo) -> ClientGroup:
    return spawn_group(g, f'responder-{zone}', {'galileo_zone': zone})


def spawn_group(g: Galileo, service_name: str = 'nginx', labels: dict = None) -> ClientGroup:
    return g.spawn(service_name, 1, parameters={'method': 'get', 'path': '/function/responder/static?time=10'}, worker_labels=labels)


def main():
    c = None
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
        c = spawn_zone_group('zone-a', galileo)
        time.sleep(1)
        client = c.clients[0]
        clear_list(client.client_id, rds)
        profile_path = './data/profiles/test.pkl'
        read_and_save_profile(profile_path, client, rds)

        def requests():
            c.request(ia=('prerecorded', client.client_id)).wait()

        run(
            g=galileo,
            telemd=telemd,
            exp=exp,
            rds=rds,
            name=f'responder-test-{int(time.time())}',
            requests=requests,
        )
    finally:
        if c is not None:
            c.close()


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
    # ctx = Context()
    # rds = ctx.create_redis()
    # g = init(rds)
    # galileo: Galileo = g['g']
    # c = spawn_group(galileo)
    # # wait_keyspace(rds)
    # read_and_save_profile(rds, c.clients[0])
    # time.sleep(1)
    # print(c.clients[0].client_id)
    # c.request(ia=('prerecorded', c.clients[0].client_id)).wait()
    # # c.request(n=5, ia=0.2).wait()
    # c.close()
