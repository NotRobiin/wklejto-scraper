from config import Config
from mongo import Database
from logger import Logger
from helper import Helper
from thread_manager import NewThread
import sys
import numpy as np
import argparse


def manage_args(cfg):
    parser = argparse.ArgumentParser()
    parser.add_argument("range", nargs=2, type=int)
    parser.add_argument("threads", nargs=1, type=int)

    args = parser.parse_args()
    cfg.RANGE = range(args.range[0], args.range[1])
    cfg.THREAD_AMOUNT = args.threads


def make_threads(cfg: Config, db: Database, helper: Helper, logger: Logger) -> list:
    amount = cfg.THREAD_AMOUNT
    ids = [list(x) for x in np.array_split(list(cfg.RANGE), amount)]

    threads = [
        NewThread(ids=ids[i], config=cfg, database=db, helper=helper, logger=logger,)
        for i in range(amount)
        if len(ids[i]) > 0
    ]

    return threads


def start_threads(threads: list) -> None:
    for t in threads:
        t.run()


def main() -> None:
    cfg = Config()

    manage_args(cfg)

    db = Database(cfg)
    db.start(confirm=True)

    helper = Helper(cfg)
    logger = Logger(config=cfg, database=db, helper=helper)
    threads = make_threads(cfg, db, helper, logger)

    start_threads(threads)


if __name__ == "__main__":
    main()
