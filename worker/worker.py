import os

import redis
from rq import Worker, Queue, Connection

listen = ['default']

redis_url = os.getenv('REDISTOGO_URL', 'redis://0.0.0.0:6379')

print("1 -------------------")
print(redis)
print("2 -------------------")
conn = redis.from_url(redis_url)

def takes_a_while(echo):
    import time
    time.sleep(1)
    print("worker doing---------------- here!! --------------")
    return echo

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
