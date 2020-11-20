from config import Config
from mongo import Database
from logger import Logger
from helper import Helper
from thread_manager import NewThread
import sys
import numpy as np


def get_range() -> list:
    args = sys.argv

    if len(args) != 2:
        return [0, 0]

    vals = [int(x) for x in args[-1].split("-")]

    return [vals[0], vals[1] + 1]


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
    cfg.set_range(get_range())

    db = Database(cfg)
    db.start(confirm=True)

    helper = Helper(cfg)
    logger = Logger(config=cfg, database=db, helper=helper)

    threads = make_threads(cfg, db, helper, logger)

    start_threads(threads)


if __name__ == "__main__":
    main()
