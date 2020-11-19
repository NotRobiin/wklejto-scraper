from scraper import Scraper
from config import Config
from mongo import Database
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

    sc = Scraper(config=cfg, database=db)
    sc.start()


if __name__ == "__main__":
    main()
