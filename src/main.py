from config import Config
from mongo import Database
from logger import Logger
from helper import Helper
from thread_manager import NewThread
import sys
import numpy as np
import argparse


def manage_args() -> dict:
    parser = argparse.ArgumentParser()
    parser.add_argument("range", nargs=2, type=int)
    parser.add_argument("threads", nargs=1, type=int)
    parser.add_argument(
        "-front",
        nargs=1,
        type=str,
        default="enabled",
        choices=["enabled", "disabled", "min"],
    )

    args = parser.parse_args()

    return {
        "range": range(args.range[0], args.range[1]),
        "threads": args.threads[0],
        "front": args.front,
    }


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
        t.start()


def main() -> None:
    # Get start-up args
    args = manage_args()

    # Update config based on args
    cfg = Config()
    cfg.THREAD_AMOUNT = args["threads"]
    cfg.RANGE = args["range"]
    cfg.FRONT_END_TYPE = args["front"][0]

    # Start database
    db = Database(cfg)
    db.start(confirm=True)

    # Start helper-functions class, logger and threads
    helper = Helper(cfg)
    logger = Logger(config=cfg, database=db, helper=helper)
    threads = make_threads(cfg, db, helper, logger)

    start_threads(threads)


if __name__ == "__main__":
    main()
