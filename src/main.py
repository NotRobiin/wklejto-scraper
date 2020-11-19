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
    r = get_range()

    if r[0] and r[1]:
        cfg.RANGE = range(r[0], r[1])

    db = Database(cfg)
    db.start(confirm=True)

    sc = Scraper(config=cfg, database=db)
    sc.start()


if __name__ == "__main__":
    main()
