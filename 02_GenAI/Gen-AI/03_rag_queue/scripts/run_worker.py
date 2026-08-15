#!/usr/bin/env python3
"""Programmatic worker launcher using `rq.SimpleWorker`.

Use this on Windows to avoid `os.fork` issues. Run from project root so
the `rag_queue` package is importable:

  python -m rag_queue.scripts.run_worker

Optional env vars:
- `REDIS_URL` (e.g. redis://localhost:6379)
- `RQ_QUEUE` (default: default)
"""
import os
from redis import Redis
from rq import SimpleWorker


def main():
    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        r = Redis.from_url(redis_url)
    else:
        r = Redis()

    queues = [os.getenv("RQ_QUEUE", "default")]
    print("Starting SimpleWorker for queues:", queues)
    worker = SimpleWorker(queues, connection=r)
    worker.work()


if __name__ == "__main__":
    main()
