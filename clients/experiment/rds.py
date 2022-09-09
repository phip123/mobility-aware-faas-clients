import redis


def wait_for_galileo_events(rds: redis.Redis):
    p = rds.pubsub( ignore_subscribe_messages=True)
    p.subscribe('galileo/events')
    for _ in p.listen():
        return


if __name__ == '__main__':
    print('Waiting for galileo events')
    rds = redis.Redis()
    wait_for_galileo_events(rds)
    print('Got some events!')