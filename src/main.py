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

    return [int(x) for x in args[-1].split("-")]


def main() -> None:
    cfg = Config()
    cfg.set_range(get_range())

    db = Database(cfg)
    db.start(confirm=True)

    helper = Helper(cfg)
    logger = Logger(config=cfg, database=db, helper=helper)

    sc = Scraper(site_id=150_000, config=cfg, database=db, helper=helper, logger=logger)
    sc.scrape()


if __name__ == "__main__":
    main()
