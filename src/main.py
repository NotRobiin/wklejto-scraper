from scraper import Scraper
from config import Config
from mongo import Database
from logger import Logger
from helper import Helper
import sys


def get_range() -> list:
    args = sys.argv

    if len(args) != 2:
        return [0, 0]

    vals = [int(x) for x in args[-1].split("-")]

    return [vals[0], vals[1] + 1]


def main() -> None:
    cfg = Config()
    cfg.set_range(get_range())

    db = Database(cfg)
    db.start(confirm=True)

    helper = Helper(cfg)
    logger = Logger(config=cfg, database=db, helper=helper)

    for i in cfg.RANGE:
        sc = Scraper(site_id=i, config=cfg, database=db, helper=helper, logger=logger)
        sc.scrape()


if __name__ == "__main__":
    main()
