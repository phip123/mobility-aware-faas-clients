import time

import redis
from galileo.shell.shell import Galileo, init, Telemd, ClientGroup, Experiment
from galileo.worker.context import Context

from clients.experiment.arrivalprofile import clear_list, read_and_save_profile
from clients.experiment.run import run


def spawn_zone_group(zone: str, g: Galileo) -> ClientGroup:
    return spawn_group(g, f'nginx-{zone}', {'galileo_zone': zone})


def spawn_group(g: Galileo, service_name: str = 'nginx', labels: dict = None) -> ClientGroup:
    return g.spawn(service_name, 1, parameters={'method': 'get', 'path': '/function/nginx'}, worker_labels=labels)


def client(profile_path: str, rds: redis.Redis, galileo: Galileo):
    c = spawn_zone_group('zone-a', galileo)
    time.sleep(1)
    client = c.clients[0]
    clear_list(client.client_id, rds)
    read_and_save_profile(profile_path, client, rds)
    return c


def main():
    clients_groups = []
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

        profile_paths = [
            './data/profiles/constant_rps_5_max_ia_1_period_1000_duration_20_delay_0.pkl',
            './data/profiles/constant_rps_5_max_ia_1_period_1000_duration_20_delay_5.pkl',
            './data/profiles/constant_rps_5_max_ia_1_period_1000_duration_20_delay_10.pkl',
            './data/profiles/constant_rps_5_max_ia_1_period_1000_duration_20_delay_10.pkl'
        ]

        for profile_path in profile_paths:
            clients_groups.append(client(profile_path, rds, galileo))

        def requests():
            for idx, group in enumerate(clients_groups):
                client = group.clients[0]
                if idx == len(clients_groups) - 1:
                    group.request(ia=('prerecorded', client.client_id)).wait()
                else:
                    group.request(ia=('prerecorded', client.client_id))

        run(
            g=galileo,
            telemd=telemd,
            exp=exp,
            rds=rds,
            name=f'test-nginx-four-clients-{int(time.time())}',
            requests=requests
        )

    finally:
        for c in clients_groups:
            c.close()
        print('done')
    # TODO call experiment.run
    # TODO update experiment.run - use telemd object to enable telemetry


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
