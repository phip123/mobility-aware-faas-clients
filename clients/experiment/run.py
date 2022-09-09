import os
import time
from typing import Callable, List, Dict

import redis
import yaml
from galileo.shell.shell import Galileo, Experiment, Telemd
from dotenv import load_dotenv, dotenv_values
from clients.experiment.k8s import start_telemd_kubernetes_adapter, stop_telemd_kubernetes_adapter
from clients.experiment.rds import wait_for_galileo_events


def read_env(env_path, params):
    try:
        values = dotenv_values(dotenv_path=env_path)
        for key, value in values.items():
            params[key] = value
    except Exception as e:
        print(e)


def read_heuristic_parameters(params: Dict):
    lbopt_env = 'osmotic_clients_lbopt_env_path'
    scale_env = 'osmotic_clients_scale_schedule_env_path'
    lbopt_path = os.getenv(lbopt_env, None)
    if lbopt_path is not None:
        read_env(lbopt_path, params)
    scale_path = os.getenv(scale_env, None)
    if scale_path is not None:
        read_env(scale_path, params)


def run(g: Galileo, telemd: Telemd, exp: Experiment, rds: redis.Redis, name: str,
        requests: Callable[[], None], params: Dict = None, hosts: List[str] = None, timeout: int = None):
    if params is None:
        params = {}
    read_heuristic_parameters(params)
    # todo manually
    # deploy worker
    # deploy service(s)
    # set services in rtbl
    # create client group
    try:
        # toggle tracing
        print("start tracing")
        g.start_tracing()

        start_ts = time.time()
        print(f"unpause telemd")
        telemd.start_telemd(hosts)

        # start exp
        print("start experiment and wait for 1 second")
        exp.start(name=name, creator='philipp', metadata=params)

        time.sleep(1)

        start_telemd_kubernetes_adapter()
        print("Waiting for telemd_kubernetes adapter to publish galileo events")
        wait_for_galileo_events(rds)
        time.sleep(1)

        # set requests
        print("start requests")
        requests()
        if timeout is not None:
            time.sleep(timeout)

        print("finished requests")

    except Exception as e:
        print(e)
    finally:
        print("stop tracing")
        g.stop_tracing()
        print("pause telemd")
        telemd.stop_telemd(hosts)
        print("stop exp")
        exp.stop()
        stop_telemd_kubernetes_adapter()
