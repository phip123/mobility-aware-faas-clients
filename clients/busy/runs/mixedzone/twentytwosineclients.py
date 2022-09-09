import json
import logging
import sys
import time

from galileo.shell.shell import Galileo, init, Telemd, Experiment
from galileo.worker.context import Context

from clients.experiment.run import run
from clients.busy.util import spawn_client_group


def main():
    params = {
        'exp': {
            'sleep': 10
        },
        'service': {
            'wait_ms': 50
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
            'data/profiles/sine_rps_5_max_ia_1_period_2_duration_80_delay_0.pkl',
            'data/profiles/sine_rps_5_max_ia_1_period_2_duration_80_delay_0.pkl',
            'data/profiles/sine_rps_5_max_ia_1_period_2_duration_80_delay_0.pkl',
            'data/profiles/sine_rps_5_max_ia_1_period_2_duration_80_delay_0.pkl',
            'data/profiles/sine_rps_5_max_ia_1_period_2_duration_80_delay_0.pkl',
            'data/profiles/sine_rps_5_max_ia_1_period_2_duration_180_delay_90.pkl',
            'data/profiles/sine_rps_5_max_ia_1_period_2_duration_360_delay_180.pkl',
            'data/profiles/sine_rps_5_max_ia_1_period_2_duration_360_delay_180.pkl',
            'data/profiles/sine_rps_5_max_ia_1_period_2_duration_360_delay_190.pkl',
            'data/profiles/sine_rps_5_max_ia_1_period_2_duration_360_delay_200.pkl',
            'data/profiles/sine_rps_5_max_ia_1_period_2_duration_360_delay_200.pkl',
        ]

        zone_b_profile_paths = [
            'data/profiles/sine_rps_5_max_ia_1_period_2_duration_180_delay_60.pkl',
            'data/profiles/sine_rps_5_max_ia_1_period_2_duration_180_delay_60.pkl',
            'data/profiles/sine_rps_5_max_ia_1_period_2_duration_180_delay_60.pkl',
            'data/profiles/sine_rps_5_max_ia_1_period_2_duration_180_delay_70.pkl',
            'data/profiles/sine_rps_5_max_ia_1_period_2_duration_180_delay_70.pkl',
            'data/profiles/sine_rps_5_max_ia_1_period_2_duration_180_delay_70.pkl',
            'data/profiles/sine_rps_5_max_ia_1_period_2_duration_180_delay_70.pkl',
            'data/profiles/sine_rps_5_max_ia_1_period_2_duration_360_delay_300.pkl',
            'data/profiles/sine_rps_5_max_ia_1_period_2_duration_360_delay_300.pkl',
            'data/profiles/sine_rps_5_max_ia_1_period_2_duration_360_delay_300.pkl',
            'data/profiles/sine_rps_5_max_ia_1_period_2_duration_400_delay_350.pkl',
        ]

        wait_ms = params['service']['wait_ms']

        clients_groups.append(
            spawn_client_group(zone_a_profile_paths, 'zone-a', rds, galileo, wait_ms))
        clients_groups.append(
            spawn_client_group(zone_b_profile_paths, 'zone-b', rds, galileo, wait_ms))

        def requests():
            for idx, group in enumerate(clients_groups):
                if idx == len(clients_groups) - 1:
                    group.request(ia=('prerecorded', 'ran')).wait()
                else:
                    group.request(ia=('prerecorded', 'ran'))
            time.sleep(int(params['exp']['sleep']))

        run(
            g=galileo,
            telemd=telemd,
            exp=exp,
            rds=rds,
            name=f'busy-mixedzone-twentytwosineclients-{int(time.time())}',
            params=params,
            requests=requests
        )

    finally:
        for c in clients_groups:
            c.close()
        print('done')


if __name__ == '__main__':
    main()
